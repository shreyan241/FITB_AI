from ninja import Router, Form
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from profiles.api.schemas.auth import UserRegistrationSchema

router = Router(tags=["auth"])

@router.post("/register", auth=None)
def register_user(request, data: UserRegistrationSchema):
    """Register a new user and return their auth token"""
    try:
        # First check if user exists
        if User.objects.filter(username=data.username).exists():
            raise HttpError(400, "Username already exists")
        
        if User.objects.filter(email=data.email).exists():
            raise HttpError(400, "Email already exists")
            
        # Create user only if doesn't exist
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            first_name=data.first_name or "",
            last_name=data.last_name or ""
        )
        
        # Create token
        token, _ = Token.objects.get_or_create(user=user)
        
        return {
            "message": "User registered successfully",
            "token": str(token.key)
        }
    except HttpError:
        raise  # Re-raise our custom errors
    except Exception as e:
        raise HttpError(500, "Failed to register user")

# Existing login endpoint
@router.post("/token", auth=None)
def get_token(request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return {"token": str(token.key)}
    raise HttpError(401, "Invalid credentials")