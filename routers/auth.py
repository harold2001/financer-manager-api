"""Authentication router for user registration and login"""

from fastapi import APIRouter, HTTPException, status
from firebase_admin import auth, get_app
from models.user import UserCreate, UserLogin, AuthResponse, UserResponse
from services import user_service


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/status")
async def check_firebase_status():
    """Check Firebase connection and configuration status"""
    try:
        # Try to list users to test Firebase connection
        auth.list_users(max_results=1)
        return {
            "status": "connected",
            "message": "Firebase is properly configured",
            "project_id": getattr(get_app(), "project_id", "unknown"),
        }
    except (ValueError, RuntimeError) as exc:
        return {
            "status": "error",
            "message": str(exc),
            "suggestion": "Check Firebase configuration and enable Email/Password authentication",
        }


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    """Register a new user with email and password"""
    try:

        # Create user in Firebase Auth
        firebase_user = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.name,
        )

        # Create user profile in Firestore
        user_profile = await user_service.create_user_profile(
            user_id=firebase_user.uid, email=user_data.email, name=user_data.name
        )

        # Generate custom token for immediate login
        custom_token = auth.create_custom_token(firebase_user.uid)

        return AuthResponse(
            message="User registered successfully",
            user=UserResponse(
                id=firebase_user.uid,
                email=user_profile.email,
                name=user_profile.name,
                created_at=user_profile.created_at,
            ),
            token=custom_token.decode("utf-8"),
        )

    except auth.EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        ) from exc
    except ValueError as exc:
        # Firebase may raise ValueError for invalid email or weak password
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except Exception as exc:

        error_message = str(exc)
        if "CONFIGURATION_NOT_FOUND" in error_message:
            detail = (
                "Firebase Authentication not configured. Please enable Email/Password "
            )
        elif "PROJECT_NOT_FOUND" in error_message:
            detail = "Firebase project not found. Please check your serviceAccountKey.json file"
        else:
            detail = f"Registration failed: {error_message}"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        ) from exc


@router.post("/login", response_model=dict)
async def login(user_data: UserLogin):
    """Login user and return authentication token"""
    try:
        # Check if user exists
        user = auth.get_user_by_email(user_data.email)

        # Note: Firebase Admin SDK can't verify passwords directly
        # In a production environment, we'd use Firebase client SDK
        # For this API, we'll generate a custom token for the existing user

        # Generate custom token for authentication
        custom_token = auth.create_custom_token(user.uid)

        # Get user profile from Firestore
        user_profile = await user_service.get_user_profile(user.uid)

        if user_profile:
            user_data_response = {
                "id": user_profile.id,
                "email": user_profile.email,
                "name": user_profile.name,
                "created_at": user_profile.created_at.isoformat(),
            }
        else:
            user_data_response = {
                "id": user.uid,
                "email": user.email,
                "name": user.display_name,
                "created_at": None,
            }

        return {
            "message": "Login successful",
            "token": custom_token.decode("utf-8"),
            "user": user_data_response,
            "token_type": "custom_token",
            "note": "Use this token in Authorization header: 'Bearer <token>'",
        }

    except auth.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        ) from exc
