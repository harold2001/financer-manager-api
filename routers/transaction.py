"""Router for transaction-related endpoints"""

from fastapi import APIRouter
from models.transaction import Transaction
from services import transaction_service as service

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/")
def create(tx: Transaction):
    """Create a new transaction"""
    return service.create_transaction(tx)

@router.get("/{user_id}")
def read(user_id: str):
    """Get all transactions for a user"""
    return service.get_transactions(user_id)

@router.put("/{tx_id}")
def update(tx_id: str, tx: Transaction):
    """Update a transaction"""
    return service.update_transaction(tx_id, tx)

@router.delete("/{tx_id}")
def delete(tx_id: str):
    """Delete a transaction"""
    return service.delete_transaction(tx_id)
