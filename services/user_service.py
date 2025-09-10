"""Service layer for user operations"""

from datetime import datetime
from typing import Optional
from config.firebase import db
from models.user import User, UserResponse, UserUpdate

users_collection = db.collection("users")


async def create_user_profile(
    user_id: str, email: str, name: Optional[str] = None
) -> User:
    """Create user profile in Firestore"""
    user_data = {"email": email, "name": name, "created_at": datetime.now()}

    # Store in Firestore with the Firebase Auth UID as document ID
    users_collection.document(user_id).set(user_data)

    return User(**user_data)


async def get_user_profile(user_id: str) -> Optional[UserResponse]:
    """Get user profile by ID"""
    doc = users_collection.document(user_id).get()

    if not doc.exists:
        return None

    user_data = doc.to_dict()
    return UserResponse(id=user_id, **user_data)


async def update_user_profile(
    user_id: str, user_update: UserUpdate
) -> Optional[UserResponse]:
    """Update user profile"""
    doc_ref = users_collection.document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    # Only update fields that are provided
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}

    if update_data:
        doc_ref.update(update_data)

    # Return updated user
    updated_doc = doc_ref.get()
    user_data = updated_doc.to_dict()
    return UserResponse(id=user_id, **user_data)


async def delete_user_profile(user_id: str) -> bool:
    """Delete user profile"""
    doc_ref = users_collection.document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        return False

    doc_ref.delete()
    return True
