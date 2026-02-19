from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional

class TransactionCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100,description="Transaction title, 3-100 chars")
    description: Optional[str] = Field(default=None, max_length=500,description='optional description, max 500 chars')
    amount: float = Field(default=0, description='amount must be greater than 0')
    type: str = Field(...,description="must be 'income' or 'expense'")
    category: str = Field(...,description="transaction category,Must not be empty, must be lowercase")
    date: datetime = Field(...,description="transaction date, can not be in  future")
    tags: Optional[List[str]] = Field(default=[], description="Max 10 tags per transaction, each tag max 30 characters")

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, i):
        if i <= 0:
            raise ValueError("Amount must be greater than 0")
        return i


    @field_validator("type")
    @classmethod
    def validate_type(cls, i):
        if i not in ["income", "expense"]:
            raise ValueError("Type must be income or expense")
        return i


    @field_validator("category")
    @classmethod
    def category_lower(cls, i):
        if not i:
            raise ValueError("Category cannot be empty")
        return i.lower()


    @field_validator("date")
    @classmethod
    def date_not_future(cls, i):
        if i > datetime.now():
            raise ValueError("Date cannot be future")
        return i


    @field_validator("tags")
    @classmethod
    def validate_tags(cls, i):
        if i and len(i) > 10:
            raise ValueError("Max 10 tags allowed")
        return i
