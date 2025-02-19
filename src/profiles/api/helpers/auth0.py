import json
from typing import Dict, Any
import httpx
from jose import jwt, jwk
from jose.exceptions import JWTError, ExpiredSignatureError
from jose.utils import base64url_decode
from django.conf import settings
from asgiref.sync import sync_to_async
from profiles.models import CustomUser
from profiles.utils.logger.logging_config import logger
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from urllib.parse import urlparse, urlunparse

# Cache for Auth0 public key
_JWKS = None
# Strip any quotes from the domain and ensure no trailing/leading whitespace
_AUTH0_DOMAIN = settings.AUTH0_DOMAIN.strip().strip("'").strip('"')

# Log environment setup
logger.info(f"Initializing Auth0 helper with domain: {_AUTH0_DOMAIN}")
logger.info(f"Auth0 audience: {settings.AUTH0_AUDIENCE}")

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jose.utils import base64url_decode
from profiles.utils.logger.logging_config import logger

def construct_public_key(n: str, e: str) -> str:
    """Construct a PEM public key from the modulus and exponent."""
    try:
        # Encode the string values to ASCII bytes before decoding
        mod_bytes = base64url_decode(n.encode('ascii'))
        exp_bytes = base64url_decode(e.encode('ascii'))
        
        modulus = int.from_bytes(mod_bytes, byteorder='big')
        exponent = int.from_bytes(exp_bytes, byteorder='big')
        
        numbers = RSAPublicNumbers(e=exponent, n=modulus)
        key = numbers.public_key(backend=default_backend())
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    except Exception as err:
        logger.error(f"Error constructing public key: {str(err)}")
        raise ValueError(f"Failed to construct public key: {str(err)}")
    
def normalize_url(url: str) -> str:
    """Normalize URL to ensure it's properly formatted"""
    parsed = urlparse(url)
    # Ensure scheme is https
    scheme = 'https'
    # Remove any double slashes (except after scheme)
    path = parsed.path.replace('//', '/')
    # Reconstruct URL with normalized components
    return urlunparse((scheme, parsed.netloc, path, '', '', ''))

async def get_auth0_public_key(token: str) -> str:
    """
    Fetch Auth0's public key to verify JWT tokens.
    Returns the PEM formatted public key.
    """
    global _JWKS
    
    try:
        # Log the token header for debugging
        header = jwt.get_unverified_header(token)
        logger.info(f"Token header kid: {header.get('kid', 'NO_KID')}")
        
        if _JWKS is None:
            try:
                # Construct and normalize the URL
                raw_url = f"https://{_AUTH0_DOMAIN}/.well-known/jwks.json"
                jwks_url = normalize_url(raw_url)
                
                async with httpx.AsyncClient(verify=True, trust_env=False) as client:
                    response = await client.get(
                        jwks_url,
                        timeout=10.0,
                        headers={'Accept': 'application/json'}
                    )
                    response.raise_for_status()
                    _JWKS = response.json()
                    logger.info("Successfully fetched JWKS")
            except httpx.HTTPError as e:
                logger.error(f"HTTP error fetching Auth0 public key: {str(e)}")
                raise ValueError(f"Failed to fetch Auth0 public key: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error fetching JWKS: {str(e)}")
                raise ValueError(f"Failed to fetch JWKS: {str(e)}")
        
        # Get the key ID from the token header
        kid = header.get('kid')
        if not kid:
            logger.error("No 'kid' found in token header")
            raise ValueError("No 'kid' found in token header")
        
        # Find the matching key in JWKS
        key = next(
            (key for key in _JWKS['keys'] if key['kid'] == kid),
            None
        )
        if not key:
            # If key not found, refresh JWKS cache and try again
            logger.warning(f"Key with kid {kid} not found in JWKS, refreshing cache")
            _JWKS = None
            return await get_auth0_public_key(token)
        
        # Convert the JWK to PEM format
        if key.get('kty') != 'RSA':
            raise ValueError(f"Unsupported key type: {key.get('kty')}")
            
        return construct_public_key(key['n'], key['e'])
        
    except Exception as e:
        logger.error(f"Error in get_auth0_public_key: {str(e)}")
        raise

async def verify_auth0_token(token: str) -> Dict[str, Any]:
    """
    Verify an Auth0 JWT token and return the payload.
    Raises an exception if the token is invalid.
    """
    try:
        logger.info(f"Starting token verification. Token starts with: {token[:10]}...")
        
        # Basic token format validation
        if not token or not isinstance(token, str):
            raise ValueError("Invalid token format")
            
        # Check token length
        if len(token) > 4096:  # Reasonable max length for JWT
            raise ValueError("Token too long")
        
        # Decode without verification first to check claims
        unverified_payload = jwt.get_unverified_claims(token)
        logger.info(f"Token audience: {unverified_payload.get('aud', 'NO_AUDIENCE')}")
            
        # Get the public key
        public_key = await get_auth0_public_key(token)
        
        # Verify the token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{_AUTH0_DOMAIN}/",
            options={
                'verify_signature': True,
                'verify_aud': True,
                'verify_iss': True,
                'verify_exp': True,
                'verify_iat': True,
                'verify_nbf': True,
                'leeway': 0  # No time leeway for validation
            }
        )
        
        logger.info("Token verified successfully")
        
        # Additional validation
        current_time = datetime.now(timezone.utc).timestamp()
        
        # Check expiration
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            if current_time > exp_timestamp:
                logger.error(f"Token expired. Expiry: {exp_timestamp}")
                raise ExpiredSignatureError("Token has expired")
                
        # Check not before time
        if 'nbf' in payload and current_time < payload['nbf']:
            raise JWTError("Token not yet valid")
            
        # Check issued at time
        if 'iat' in payload:
            issued_at = payload['iat']
            if current_time < issued_at:
                raise JWTError("Token issued in the future")
                
        # Only verify sub claim is present
        if 'sub' not in payload:
            raise ValueError("Token missing required claim: sub")
        
        return payload
        
    except ExpiredSignatureError as e:
        logger.warning(f"Token expired: {str(e)}")
        raise
    except JWTError as e:
        logger.error(f"JWT validation error: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Error verifying Auth0 token: {str(e)}")
        raise

@sync_to_async
def get_or_create_user_from_auth0(auth0_user: Dict[str, Any]) -> CustomUser:
    """
    Get or create a user based on Auth0 user data.
    Only uses sub and email fields.
    """
    try:
        # Extract user data from Auth0 payload
        auth0_id = auth0_user['sub']
        email = auth0_user.get('email', '').lower() if auth0_user.get('email') else f"{auth0_id}@auth0.user"
        
        # Try to get existing user by Auth0 ID or email
        user = None
        if auth0_id:
            user = CustomUser.objects.filter(auth0_id=auth0_id).first()
        if not user and email:
            user = CustomUser.objects.filter(email=email).first()
            
        if user:
            # Update existing user
            user.auth0_id = auth0_id
            user.email = email
            user.save(update_fields=['auth0_id', 'email'])
        else:
            # Create new user
            user = CustomUser.objects.create(
                auth0_id=auth0_id,
                email=email
            )
            
        return user
    except Exception as e:
        logger.error(f"Error creating/updating user from Auth0: {str(e)}")
        raise 