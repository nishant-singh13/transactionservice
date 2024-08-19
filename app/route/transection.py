from fastapi import APIRouter, Depends, HTTPException,  Path
from sqlalchemy.orm import Session

from .. services import transection
from ..database.db import get_db
from ..schemas.transection.request import Create
from ..schemas.transection.response import Response, SumResponse

router = APIRouter(
    prefix='/transactionservice',
    tags=['Transactions API']
)


@router.put("/transaction/{transaction_id}", response_model=Response)
def create_transaction(transaction_id: int, data: Create, db: Session = Depends(get_db)):
    db_transaction = transection.get_transaction(db, transaction_id)

    # Validate that the transaction ID exists if provided
    if db_transaction:
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    # Validate that the parent_id exists if provided
    if data.parent_id is not None:
        print("parent data id ", data.parent_id)
        parent_transaction = transection.get_transaction(db, data.parent_id)
        if parent_transaction is None:
            raise HTTPException(status_code=400, detail="Parent transaction not found")

    # Approach 2 using extra table to maintain ..  ancestor_id , descendant_id relation
    # just uncomment blow code for testing
    # return transection.create_v2(db, data, transaction_id)

    # Approach 1 using parent child relation into single table
    return transection.create(db, data, transaction_id)


@router.get("/transaction/{transaction_id}", response_model=Response)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transection.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/types/{transaction_type}", response_model=list[Response])
def get_transactions_by_type(transaction_type: str, db: Session = Depends(get_db)):
    transactions = transection.get_transactions_by_type(db, transaction_type)
    return transactions


@router.get("/sum/{transaction_id}", response_model=SumResponse)
def get_transaction_sum(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transection.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # Approach 1 using parent child relation into single table ... using rec/queue to compute result
    total_sum = transection.calculate_sum(db, transaction_id)
    # Approach 2 using extra table to maintain ..  ancestor_id , descendant_id relation
    # just uncomment blow code for testing
    # total_sum = transaction.calculate_sum_using_closure(db, transaction_id)
    return SumResponse(sum=total_sum)
