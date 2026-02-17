from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    type: str
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    type: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    name: str
    type: str
    description: Optional[str]