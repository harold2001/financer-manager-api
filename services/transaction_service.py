"""Service layer for transaction operations"""

from datetime import datetime
from typing import Optional, List
from config.firebase import db
from models.transaction import Transaction, TransactionResponse, TransactionUpdate

collection = db.collection("transactions")


async def create_transaction(transaction: Transaction) -> TransactionResponse:
    """Create a new transaction"""
    doc_ref = collection.document()
    transaction_data = transaction.dict()
    doc_ref.set(transaction_data)

    return TransactionResponse(id=doc_ref.id, **transaction_data)


async def get_transaction(transaction_id: str) -> Optional[TransactionResponse]:
    """Get a single transaction by ID"""
    doc = collection.document(transaction_id).get()

    if not doc.exists:
        return None

    transaction_data = doc.to_dict()
    return TransactionResponse(id=transaction_id, **transaction_data)


async def get_user_transactions(
    user_id: str,
    transaction_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
) -> List[TransactionResponse]:
    """Get all transactions for a user with optional filters"""
    query = collection.where("user_id", "==", user_id)

    # Apply filters
    if transaction_type:
        query = query.where("type", "==", transaction_type)

    if category:
        query = query.where("category", "==", category)

    if start_date:
        query = query.where("date", ">=", start_date)

    if end_date:
        query = query.where("date", "<=", end_date)

    # Order by date (newest first)
    query = query.order_by("date", direction="DESCENDING")

    docs = query.stream()
    transactions = []

    for doc in docs:
        transaction_data = doc.to_dict()
        transactions.append(TransactionResponse(id=doc.id, **transaction_data))

    return transactions


async def update_transaction(
    transaction_id: str, transaction_update: TransactionUpdate
) -> TransactionResponse:
    """Update a transaction"""
    doc_ref = collection.document(transaction_id)

    # Only update fields that are provided (not None)
    update_data = {k: v for k, v in transaction_update.dict().items() if v is not None}

    if update_data:
        doc_ref.update(update_data)

    # Return updated transaction
    updated_doc = doc_ref.get()
    transaction_data = updated_doc.to_dict()
    return TransactionResponse(id=transaction_id, **transaction_data)


async def delete_transaction(transaction_id: str) -> bool:
    """Delete a transaction"""
    doc_ref = collection.document(transaction_id)
    doc = doc_ref.get()

    if not doc.exists:
        return False

    doc_ref.delete()
    return True


# Legacy functions for backward compatibility (remove if not needed)
def create_transaction_sync(tx: Transaction):
    """Legacy sync function - deprecated"""
    doc_ref = collection.document()
    doc_ref.set(tx.dict())
    return {"id": doc_ref.id, **tx.dict()}


def get_transactions_sync(user_id: str):
    """Legacy sync function - deprecated"""
    docs = collection.where("user_id", "==", user_id).stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]


def update_transaction_sync(tx_id: str, tx: Transaction):
    """Legacy sync function - deprecated"""
    doc_ref = collection.document(tx_id)
    doc_ref.update(tx.dict())
    return {"id": tx_id, **tx.dict()}


def delete_transaction_sync(tx_id: str):
    """Legacy sync function - deprecated"""
    collection.document(tx_id).delete()
    return {"id": tx_id, "deleted": True}
