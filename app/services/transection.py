from sqlalchemy.orm import Session
from ..model.transection import Transaction, TransactionClosure
from ..schemas.transection.request import Create
from sqlalchemy import text


def create(db: Session, transaction: Create, transaction_id: int):
    """
    First Approach
    This function handles the creation of a new transaction in O(1) time as it only involves inserting a new record into the `transactions` table.
    Advantage: Insertion is done in O(1) time. This approach works better if the system has more insertions compared to querying the SUM of transactions, especially when there is a deeper parent-child hierarchy.

    :param transaction_id: transaction id
    :param db : SQL session object for database operations.
    :param transaction: transaction (TransactionCreate): Pydantic model containing the transaction data.

    :returns: Transaction: The created Transaction object.

    :raises: HTTPException: If any database operation fails, the transaction is rolled back, and an error is raised.

    """

    db_transaction = Transaction(
        id=transaction_id,
        amount=transaction.amount,
        type=transaction.type,
        parent_id=transaction.parent_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transaction(db: Session, transaction_id: int):
    """
    This function checking is transaction exit in our system or not.
    in O(1) time complexity as we are looking up on primiry key

    :param db : SQL session object for database operations.
    :param transaction_id: transaction ID
    :return:  Transaction object that match the transaction id

    """
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_transaction_by_parent(db: Session, parent_id: int) -> [Transaction]:
    """
    :param db : SQL session object for database operations.
    :param : transaction ID
    :return:  Transaction object that match the transaction id
    """
    print(" parent query -------", parent_id )
    return db.query(Transaction).filter(Transaction.parent_id == parent_id).all()


def get_transactions_by_type(db: Session, transaction_type: str):
    """
    Fetches all transactions from the database that match the given type.
    O(n) - where 'n' is the number of transactions in the database.
    This is because the function must scan all transactions to filter out those that match the given type.

    :param: db : The database session used to perform the query.
    :param : transaction_type (str): The type of transactions to filter by.

    :returns: List[Transaction]: A list of transactions that match the specified type.
    """

    return db.query(Transaction).filter(Transaction.type == transaction_type).all()


def calculate_sum(db: Session, transaction_id: int) -> float:
    """
    Queue-based Approach:
    This function calculates the sum of all transactions linked to a given transaction using an iterative approach with a queue.

    :param db: SQL session object for database operations.
    :param transaction_id: transaction ID
    :return : sum of all transaction . part of current tree -parent- chile tree

    Time Complexity:
        O(n) - where 'n' is the number of linked transactions.
    Space Complexity:
        O(n) - extra space is required for the queue to store transactions.

    Advantage over Recursive Approach:
        - This iterative queue-based approach avoids recursion depth limits and generally performs better in terms of memory usage.
        - It handles large trees of transactions without hitting the recursion limit, making it more suitable for deep hierarchies.
    Potential Drawbacks:
        - we are making n query to DB which is not a good option if we have too may child in a tree
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return 0.0

    # Creating a queue and pushing the root parent transaction
    queue = [transaction]
    sum = 0.0

    while len(queue) != 0:
        number_of_child = len(queue)
        # If this node has children
        while number_of_child > 0:
            transaction = queue[0]
            queue.pop(0)
            sum += transaction.amount
            print("childer ---------", transaction.id)
            childrens = get_transaction_by_parent(db, transaction.id)
            print("childer ---------", childrens)
            # push all children of the queue item
            if len(childrens) > 0:
                queue += childrens
            number_of_child = number_of_child - 1
    return sum


def calculate_sum_v2(db: Session, transaction_id: int) -> float:
    """
    Recursive Approach using SQL:
    This function calculates the sum of all transactions linked to a given transaction using a recursive SQL query.

    :param db: SQL session object for database operations.
    :param transaction_id: transaction ID
    :return : sum of all transaction . part of current tree -parent- chile tree

    Time Complexity:
        O(n) - where 'n' is the number of linked transactions.

    Space Complexity:
        O(1) - The SQL query is executed in constant space without extra data structures.

    Advantage:
        - The recursive SQL query is optimized within the database engine and can be faster for smaller or moderate-sized datasets.
        - It leverages SQL's native recursion capabilities to handle the hierarchy in a more straightforward manner.

    Potential Drawbacks:
        - This approach might hit performance limits if the hierarchy is too deep or if the dataset is very large.
    """

    query = text("""
        WITH RECURSIVE linked_transactions AS (
            SELECT id, amount, parent_id FROM transactions WHERE id = :transaction_id
            UNION ALL
            SELECT t.id, t.amount, t.parent_id
            FROM transactions t
            INNER JOIN linked_transactions lt ON lt.id = t.parent_id
        )
        SELECT SUM(amount) FROM linked_transactions;
    """)
    result = db.execute(query, {"transaction_id": transaction_id}).scalar()
    total_sum = result if result else 0.0
    return total_sum

# TODO second Approach .. how we can handle parent child relation .. if we have more read and we need data much faster


def create_v2(db: Session, transaction: Create, transaction_id: int):
    """
    Second Approach
    This function handles the creation of a new transaction and updates the transaction closure table
    to maintain the ancestor-descendant relationships.

    :param transaction_id: transaction id
    :param db: SQL session object for database operations
    :param transaction: transaction (TransactionCreate): Pydantic model containing the transaction data.

    :returns: Transaction: The created Transaction object.

    :raises:    HTTPException: If any database operation fails, the transaction is rolled back, and an error is raised.
    """
    # Step 1: Insert into the transactions table
    db_transaction = Transaction(id=transaction_id,  amount=transaction.amount, type=transaction.type, parent_id=transaction.parent_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # Step 2: Insert into the transaction_closure table
    # Insert self-relation
    db.add(TransactionClosure(ancestor_id=db_transaction.id, descendant_id=db_transaction.id))

    # Insert ancestor relationships if parent_id is not None
    if transaction.parent_id is not None:
        ancestors = db.query(TransactionClosure).filter(TransactionClosure.descendant_id == transaction.parent_id).all()
        for ancestor in ancestors:
            db.add(TransactionClosure(ancestor_id=ancestor.ancestor_id, descendant_id=db_transaction.id))

    db.commit()
    return db_transaction


def calculate_sum_using_closure(db: Session, transaction_id: int) -> float:
    """
    Calculates the sum of all transactions that are descendants of the given transaction
    using the TransactionClosure table.

    Args:
        db (Session): The database session used to perform the query.
        transaction_id (int): The ID of the root transaction.

    Returns:
        float: The sum of all amounts for the given transaction and its descendants.

    Time Complexity:
        O(n) - where 'n' is the number of descendants (including the root transaction).
    """

    query =  text("""
        SELECT SUM(t.amount)
        FROM transactions t
        INNER JOIN transaction_closure tc ON t.id = tc.descendant_id
        WHERE tc.ancestor_id = :transaction_id;
    """)

    result = db.execute(query, {"transaction_id": transaction_id}).scalar()
    total_sum = result if result else 0.0  # Return 0 if the sum is None (no transactions found)
    return total_sum
