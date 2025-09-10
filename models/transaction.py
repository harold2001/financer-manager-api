"""Transaction model for financial records"""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Base transaction model"""

    type: Literal["income", "expense"]
    amount: float = Field(gt=0, description="Amount must be positive")
    category: str = Field(min_length=1, description="Category is required")
    date: datetime
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    """Transaction creation model"""


class TransactionUpdate(BaseModel):
    """Transaction update model"""

    type: Optional[Literal["income", "expense"]] = None
    amount: Optional[float] = Field(None, gt=0, description="Amount must be positive")
    category: Optional[str] = Field(None, min_length=1)
    date: Optional[datetime] = None
    description: Optional[str] = None


class Transaction(TransactionBase):
    """A financial transaction record"""

    user_id: str


class TransactionResponse(TransactionBase):
    """Transaction response model"""

    id: str
    user_id: str
