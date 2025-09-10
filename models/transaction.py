"""Transaction model for financial records"""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel

class Transaction(BaseModel):
    """A financial transaction record"""
    user_id: str
    type: Literal["income", "expense"]
    amount: float
    date: datetime
