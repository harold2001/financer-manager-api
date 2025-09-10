"""Authentication middleware for Firebase JWT validation"""

import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

logger = logging.getLogger(__name__)

security = HTTPBearer()


class AuthMiddleware:
    """Middleware for Firebase JWT authentication"""

    @staticmethod
    def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ) -> dict:
        """Verify Firebase JWT token and return user claims"""
        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(credentials.credentials)
            return decoded_token
        except auth.ExpiredIdTokenError as exc:
            logger.error("Expired ID token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except auth.InvalidIdTokenError as exc:
            logger.error("Invalid ID token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except Exception as exc:
            logger.error("Token verification failed: %s", str(exc))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    @staticmethod
    def get_current_user(token_data: dict = Depends(verify_token)) -> str:
        """Get current user ID from token"""
        user_id = token_data.get("uid")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user ID not found",
            )
        return user_id


# Convenience function for dependency injection
def get_current_user_id(token_data: dict = Depends(AuthMiddleware.verify_token)) -> str:
    """Get current user ID from authenticated token"""
    return AuthMiddleware.get_current_user(token_data)
