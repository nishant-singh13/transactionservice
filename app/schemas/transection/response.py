from pydantic import BaseModel
from typing import Optional


class Response(BaseModel):
    id: int
    amount: float
    type: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class SumResponse(BaseModel):
    sum: float

