import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from main import app
from app.model.transection import Transaction
from app.database.db import get_db  # Assuming get_db is the dependency function that provides the DB session


# Fixture to create the mock database
@pytest.fixture(scope="function")
def mock_db():
    db = MagicMock()
    return db


# Fixture to reset the mock between tests
@pytest.fixture(scope="function", autouse=True)
def reset_mocks(mock_db):
    mock_db.reset_mock()


# Fixture to create the test client
@pytest.fixture(scope="function")
def test_client(mock_db):
    # Override the dependency with the mock
    app.dependency_overrides[get_db] = lambda: mock_db
    return TestClient(app)


def test_create_transaction(test_client, mock_db):
    # Mock the behavior of querying the database to ensure no transaction with the same ID exists
    mock_db.query().filter().first.return_value = None

    # Mock the transaction creation and return the mock transaction
    mock_transaction = Transaction(id=1, amount=100.0, type="expense", parent_id=None)
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_transaction

    # Make the PUT request to create the transaction
    response = test_client.put("/transactionservice/transaction/1", json={"amount": 100.0, "type": "expense"})

    # Print and assert the response
    print(response.json())  # Inspect the response for debugging
    assert response.status_code == 200
    assert response.json() == {"id": 1, "amount": 100.0, "type": "expense", "parent_id": None}

    # Reset the overrides after the test
    app.dependency_overrides = {}


def test_get_transactions_by_type(test_client, mock_db):
    # Mock data as Transaction objects
    mock_transactions = [
        Transaction(id=1, amount=100.0, type="expense", parent_id=None),
        Transaction(id=2, amount=200.0, type="expense", parent_id=None)
    ]
    # Set up mock return value for query
    mock_db.query(Transaction).filter(Transaction.type == "expense").all.return_value = mock_transactions

    # Perform the GET request
    response = test_client.get("/transactionservice/types/expense")

    # Assertions
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "amount": 100.0, "type": "expense", "parent_id": None},
        {"id": 2, "amount": 200.0, "type": "expense", "parent_id": None}
    ]


def test_get_transaction(test_client, mock_db):
    mock_transaction = Transaction(id=1, amount=100.0, type="expense", parent_id=None)
    mock_db.query(Transaction).filter(Transaction.id == 1).first.return_value = mock_transaction
    response = test_client.get("/transactionservice/transaction/1")
    print("Actual Response:", response.json())  # Debug the response
    assert response.status_code == 200
    assert response.json() == {"id": 1, "amount": 100.0, "type": "expense", "parent_id": None}
    app.dependency_overrides = {}


def test_create_transaction_with_invalid_amount_data(test_client):
    response = test_client.put("/transactionservice/transaction/1", json={"amount": "0", "type": "expense"})
    assert response.status_code == 422


def test_create_transaction_with_invalid_type_data(test_client):
    response = test_client.put("/transactionservice/transaction/1", json={"amount": "0", "type": ""})
    assert response.status_code == 422


def test_create_transaction_with_invalid_parent_id_data(test_client):
    response = test_client.put("/transactionservice/transaction/1",
                               json={"amount": "0", "type": "string", "parent_id": 0})
    assert response.status_code == 422


def test_get_nonexistent_transaction(test_client, mock_db):
    mock_db.query(Transaction).filter(Transaction.id == 1).first.return_value = None

    response = test_client.get("/transactionservice/transaction/999")
    assert response.status_code == 404  # Not Found


def test_get_transaction_sum_no_linked_transaction(test_client, mock_db):
    mock_transactions = [
        Transaction(id=1, amount=100.0, type="expense", parent_id=None)
    ]

    mock_db.query(Transaction).filter(Transaction.id == 1).first.return_value = mock_transactions[0]

    response = test_client.get("/transactionservice/sum/1")
    assert response.status_code == 200
    assert response.json() == {"sum": 100.0}


@patch('app.database.db', autospec=True)
@patch('app.services.transection.get_transaction_by_parent')
def test_get_transaction_sum_by_parent_child_relation(mock_db, mock_get_transaction_by_parent):
    # Define mock transactions
    mock_transactions = [
        Transaction(id=1, amount=10.0, type="expense", parent_id=None),
        Transaction(id=2, amount=20.0, type="expense", parent_id=1),
        Transaction(id=3, amount=30.0, type="expense", parent_id=1),
        Transaction(id=4, amount=40.0, type="expense", parent_id=2)
    ]

    # Mock `get_transaction_by_parent` to return the appropriate transactions based on parent_id
    def mock_get_transaction_by_parent_func(parent_id):
        return [tx for tx in mock_transactions if tx.parent_id == parent_id]

    mock_get_transaction_by_parent.side_effect = mock_get_transaction_by_parent_func

    mock_db.query(Transaction).filter(Transaction.id == 1).first.return_value = mock_transactions[0]
    client = TestClient(app)
    response = client.get("/transactionservice/sum/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"sum": 100.0}

    # Clean up the mock
    patch.stopall()


def test_get_transaction_sum_with_invalid_id(test_client, mock_db):
    mock_db.query(Transaction).filter(Transaction.id == 999).first.return_value = None

    response = test_client.get("/transactionservice/sum/999")
    assert response.status_code == 404  # Not Found


# Clean up dependency overrides after tests
@pytest.fixture(scope="function", autouse=True)
def clean_up_dependency_overrides():
    yield
    app.dependency_overrides = {}
