"""Service layer for transaction operations"""

from config.firebase import db
from models.transaction import Transaction

collection = db.collection("transactions")

def create_transaction(tx: Transaction):
    doc_ref = collection.document()
    doc_ref.set(tx.dict())
    return {"id": doc_ref.id, **tx.dict()}

def get_transactions(user_id: str):
    docs = collection.where("user_id", "==", user_id).stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]

def update_transaction(tx_id: str, tx: Transaction):
    doc_ref = collection.document(tx_id)
    doc_ref.update(tx.dict())
    return {"id": tx_id, **tx.dict()}

def delete_transaction(tx_id: str):
    collection.document(tx_id).delete()
    return {"id": tx_id, "deleted": True}
