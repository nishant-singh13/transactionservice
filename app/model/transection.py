from sqlalchemy import Column, Double, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.database.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(BigInteger, primary_key=True, index=True)
    amount = Column(Double, nullable=False)
    type = Column(String, index=True, nullable=False)
    parent_id = Column(BigInteger, ForeignKey('transactions.id'), nullable=True)


'''
The design of these two classes, Transaction and TransactionClosure, is an implementation of a closure
table pattern to manage hierarchical data, particularly to model parent-child relationships in the database. 

The Closure Table solution is an elegant way of storing hierarchies that trade-off space complexity for query and time efficiency. 
It involves storing all paths that exist in the tree in a separate table, unlike adjacency lists which only store the parent-child path.

Advantage: 
if you want to find all transactions linked to a particular transaction (including all levels of descendants),
you can do this with a simple query on the transaction_closure table

Disadvantages: 
- In a large system with many transactions and deep hierarchies, the closure table could become large,
leading to increased storage costs and potentially slower performance on certain operations like bulk inserts or updates.
- If the system has more writes than reads, particularly more insertions and updates compared to queries for summing transactions,
 the closure table approach might not be the optimal solution.  
'''


class TransactionClosure(Base):
    __tablename__ = "transaction_closure"

    ancestor_id = Column(BigInteger, ForeignKey('transactions.id'), primary_key=True)
    descendant_id = Column(BigInteger, ForeignKey('transactions.id'), primary_key=True)
