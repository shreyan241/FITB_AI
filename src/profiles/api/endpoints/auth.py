from ninja import Router
from ninja.errors import HttpError
from profiles.api.helpers.auth0 import verify_auth0_token, get_or_create_user_from_auth0, normalize_url
from profiles.api.schemas.auth import Auth0TokenSchema, UserResponse
from profiles.utils.logger.logging_config import logger
import httpx
from django.conf import settings

router = Router(tags=["auth"])

@router.post("/auth0/verify", auth=None, response=UserResponse)
async def verify_auth0_user(request, data: Auth0TokenSchema):
    """Verify Auth0 token and get or create user"""
    try:
        # Verify the Auth0 token
        auth0_token = await verify_auth0_token(data.token)
        
        # Construct and normalize the userinfo URL
        userinfo_url = normalize_url(f"https://{settings.AUTH0_DOMAIN}/userinfo")
        logger.info(f"Fetching userinfo from: {userinfo_url}")
        
        # Fetch userinfo using the token
        try:
            async with httpx.AsyncClient(trust_env=False) as client:
                userinfo_response = await client.get(
                    userinfo_url,
                    headers={"Authorization": f"Bearer {data.token}"},
                    timeout=10.0
                )
                userinfo_response.raise_for_status()
                userinfo = userinfo_response.json()
                logger.info("Successfully fetched userinfo")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching userinfo: {str(e)}")
            raise HttpError(401, "Failed to fetch user info")
        except Exception as e:
            logger.error(f"Unexpected error fetching userinfo: {str(e)}")
            raise HttpError(401, "Failed to fetch user info")
        
        # Get or create user from userinfo
        user = await get_or_create_user_from_auth0(userinfo)
        
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name if hasattr(user, 'first_name') else None,
            last_name=user.last_name if hasattr(user, 'last_name') else None,
            is_verified=user.is_verified if hasattr(user, 'is_verified') else False,
            auth0_id=user.auth0_id
        )
    except Exception as e:
        logger.error(f"Error verifying Auth0 token: {str(e)}")
        if isinstance(e, HttpError):
            raise
        raise HttpError(401, "Invalid Auth0 token")