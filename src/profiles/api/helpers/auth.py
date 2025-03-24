from django.core.exceptions import PermissionDenied
from asgiref.sync import sync_to_async
from profiles.models import UserProfile
from profiles.utils.logger.logging_config import logger
from ninja.security import HttpBearer
from django.core.exceptions import ValidationError
from jose.exceptions import ExpiredSignatureError
from profiles.api.helpers.auth0 import verify_auth0_token, get_or_create_user_from_auth0
from ninja.errors import HttpError

class Auth0BearerAuth(HttpBearer):
    async def authenticate(self, request, token):
        """
        Authenticate the request using Auth0 token.
        Args:
            request: The HTTP request
            token: The Bearer token from the Authorization header
        Returns:
            CustomUser: The authenticated user
        Raises:
            HttpError: If authentication fails
        """
        if not token:
            return None
            
        try:
            # Verify Auth0 token
            auth0_user = await verify_auth0_token(token)
            
            # Get or create user from Auth0 data
            user = await get_or_create_user_from_auth0(auth0_user)
            
            if not user.is_active:
                raise HttpError(403, "User account is disabled")
            
            # Attach user to request
            request.user = user
            return user
            
        except ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except ValueError as e:
            raise HttpError(401, str(e))
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HttpError(401, "Invalid authentication credentials")

async def check_auth_and_staff(request):
    """
    Check if user is authenticated and is staff.
    Args:
        request: The HTTP request object
    Raises:
        PermissionDenied: If user is not authenticated or not staff
    """
    # Check authentication
    is_authenticated = await sync_to_async(lambda: request.user.is_authenticated)()
    if not is_authenticated:
        raise PermissionDenied("Authentication required")
    
    # Check staff status
    is_staff = await sync_to_async(lambda: request.user.is_staff)()
    if not is_staff:
        logger.warning(f"Non-staff access attempt by user {request.user.id}")
        raise PermissionDenied("Staff access required")

async def get_profile_with_auth_check(request, profile_id: int, action: str = "access") -> UserProfile:
    """
    Get profile and check if the user has permission to access it.
    Args:
        request: The request object containing auth user
        profile_id: The ID of the profile to check
        action: The action being performed (for error message)
    Returns:
        UserProfile: The profile if access is allowed
    Raises:
        ValidationError: If profile not found or user doesn't have permission
    """
    if not request.user.is_authenticated:
        raise ValidationError("Authentication required")
        
    try:
        profile = await UserProfile.objects.select_related('user').aget(id=profile_id)
        
        # Check permissions
        is_superuser = await sync_to_async(lambda: request.user.is_superuser)()
        profile_user = await sync_to_async(lambda: profile.user)()
        
        if not (is_superuser or profile_user == request.user):
            logger.warning(
                f"Unauthorized profile access attempt: user {request.user.id} "
                f"tried to {action} profile {profile_id}"
            )
            raise ValidationError(f"You don't have permission to {action} this profile")
            
        return profile
    except UserProfile.DoesNotExist:
        raise ValidationError("Profile not found") 