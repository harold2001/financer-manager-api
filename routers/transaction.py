"""Router for transaction-related endpoints"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from models.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    Transaction,
)
from services import transaction_service
from middleware.auth import get_current_user_id

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user_id: str = Depends(get_current_user_id),
):
    """Create a new transaction for the authenticated user"""
    # Create transaction with user_id from auth token
    transaction = Transaction(user_id=current_user_id, **transaction_data.dict())

    return await transaction_service.create_transaction(transaction)


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    current_user_id: str = Depends(get_current_user_id),
    transaction_type: Optional[str] = Query(None, regex="^(income|expense)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    category: Optional[str] = Query(None),
):
    """Get all transactions for the authenticated user with optional filters"""
    return await transaction_service.get_user_transactions(
        user_id=current_user_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        category=category,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str, current_user_id: str = Depends(get_current_user_id)
):
    """Get a single transaction by ID (must belong to authenticated user)"""
    transaction = await transaction_service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    # Ensure transaction belongs to current user
    if transaction.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this transaction",
        )

    return transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user_id: str = Depends(get_current_user_id),
):
    """Update a transaction (must belong to authenticated user)"""
    # First check if transaction exists and belongs to user
    existing_transaction = await transaction_service.get_transaction(transaction_id)

    if not existing_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    if existing_transaction.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this transaction",
        )

    return await transaction_service.update_transaction(
        transaction_id, transaction_update
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str, current_user_id: str = Depends(get_current_user_id)
):
    """Delete a transaction (must belong to authenticated user)"""
    # First check if transaction exists and belongs to user
    existing_transaction = await transaction_service.get_transaction(transaction_id)

    if not existing_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    if existing_transaction.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this transaction",
        )

    await transaction_service.delete_transaction(transaction_id)
    return None
