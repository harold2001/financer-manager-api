"""User router for profile management"""

from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserResponse, UserUpdate
from services import user_service
from middleware.auth import get_current_user_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user_id: str = Depends(get_current_user_id)):
    """Get current logged-in user profile"""
    user = await user_service.get_user_profile(current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )

    return user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate, current_user_id: str = Depends(get_current_user_id)
):
    """Update current user profile"""
    user = await user_service.update_user_profile(current_user_id, user_update)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found"
        )

    return user
