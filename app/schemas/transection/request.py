from pydantic import BaseModel
from typing import Optional
from pydantic import validator


class Create(BaseModel):
    amount: float
    type: str
    parent_id: Optional[int] = None

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        return v

    @validator('type')
    def validate_type(cls, v):
        if not v.strip():
            raise ValueError('Type cannot be empty')
        return v

    @validator('parent_id')
    def validate_parent_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError('Parent ID must be greater than zero.')
        return value
