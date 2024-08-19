# Transaction Service
We would like to have a RESTful web service that stores some transactions (in memory is fine) and
returns information about those transactions. The transactions to be stored have a type and an
amount. The service should support returning all transactions of a type. Also, transactions can be
linked to each other (using a ”parent id”) and we need to know the total amount involved for all
transactions linked to a particular transaction.

# NOTE : Asymptotic Complexity of Parent-Child Tree Operations
When dealing with parent-child trees, understanding the asymptotic complexity of various operations is crucial for efficient design and implementation. In this context, we explore two distinct approaches for managing hierarchical relationships in transactions, each with its own characteristics and performance implications.

## Implementation Approaches

## 1. Single Table Parent-Child Approach
In this approach, the Transaction table uses a single table to store both parent and child transactions. Each transaction has a parent_id field that links it to its parent transaction, if applicable. This design supports hierarchical transactions where each transaction can have multiple children, and queries can retrieve all related transactions by traversing these links.

- Advantages:

Simplicity in design and implementation.
Direct representation of hierarchical relationships in a single table.

- Disadvantages:

Performance can degrade with deep or unbalanced hierarchies due to potentially high traversal costs.
Recursive queries may be complex and less efficient in some database systems.

## 2. TransactionClosure Table Approach
The TransactionClosure table approach involves using an additional table, TransactionClosure, to efficiently query hierarchical relationships. This table stores all ancestor-descendant relationships for each transaction, enabling fast retrieval of all transactions linked to a particular transaction, including indirect links. This approach is particularly useful for complex hierarchies and large datasets, offering better performance for certain types of queries.

- Advantages:

Fast retrieval of hierarchical data due to precomputed ancestor-descendant relationships.
Efficient querying of complex hierarchies and large datasets.

- Disadvantages:

Increased complexity in design and implementation due to the additional closure table.
Additional storage and maintenance overhead for keeping the closure table updated.



## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

To set up and run the transactions service server, follow these steps:

### 1. Clone the Repository

```console
git clone https://github.com/nishant-singh13/transactionservice.git
cd  transactionservice
```
## 2. ADD .env file on you local machine 
```console
DATABASE_URL = ""
```

## 3. Build and Run with Docker Compose
Ensure Docker and Docker Compose are installed and running on your system. Then, use Docker Compose to build and start the services:


```console
docker-compose up --build
```

## 4. Access the Application
Once the containers are up, you can access the application at http://localhost:8000 (or whichever port is specified in your docker-compose.yml file).

## 5. Swagger UI
For API documentation and interactive testing, you can use the Swagger UI at the following link: 
Here is swagger link : http://0.0.0.0:8000/docs

## 6 . Stopping the Server
To stop the running Docker containers, use:


```console
docker-compose down
```

## 7. API Endpoints
Here are the API endpoints supported by the service:
Create Transaction
```
PUT /transactionservice/transaction/{transaction_id}

```

Get Transaction By Id

```
GET /transactionservice/transaction/{transaction_id}

```

Get Transactions By Type
```
GET /transactionservice/types/{transaction_type}

```
Get Transaction Sum
```
GET /transactionservice/sum/{transaction_id}
```




## 8. Test Cases
To ensure the correctness and functionality of the transactions service, you should write and run test cases. Here are some example test cases you might consider implementing:

8.1. Test Case: Add a Transaction
Description: Verify that a transaction can be added and stored correctly.

Endpoint: PUT /transactionservice/transaction/{transection_id}

Request Body:
```
{
  "amount": 10,
  "type": "string",
  "parent_id": 0  // null or non zero value ootional 
}
```
Expected Response:

```
Status Code: 200 Created
Response Body: (Contains details of the created transaction)
{
    "id": 111,
    "amount": 10.0,
    "type": "string",
    "parent_id": null
}
```

8.2. Test Case: Retrieve Transactions by Types
Description: Ensure that transactions can be retrieved based on their type.
```
Endpoint: GET /transactionservice/types/{transaction_type}
```
Example Request:
```
curl -X GET "http://localhost:8000/transactionservice/types/expense"
Expected Response:


Status Code: 200 OK
Response Body: (List of transactions with the specified type)
[
    {
        "id": 26,
        "amount": 10.0,
        "type": "string",
        "parent_id": null
    },
    {
        "id": 10,
        "amount": 10.0,
        "type": "string",
        "parent_id": null
    }
]
```


8.3. Test Case: Retrieve transection by  Transaction id 
Description: Verify that the total amount for all transactions linked to a specific transaction is calculated correctly.


Endpoint: GET /transactionservice/transaction/{transaction_id}

Example Request:
```
curl -X GET "http://localhost:8000/transactionservice/transactions/1"
Expected Response:

Status Code: 200 OK
Response Body: transactions  object 
{
    "id": 10,
    "amount": 10.0,
    "type": "string",
    "parent_id": null
}
```


8.4. Test Case: get total transection value -- parent child 
Description: Verify that the total amount for all transactions linked to a specific transaction is calculated correctly.


Endpoint: GET GET /transactionservice/sum/{transaction_id}

Example Request:
```
curl -X GET "http://localhost:8000/transactionservice/sum/1"
Expected Response:

Status Code: 200 OK
Response Body: {"sum": 100.0} 
```


## 9 Running Tests
## Unit Tests: Ensure your unit tests are written to cover the functionality of the service. You can use testing frameworks like pytest for Python.

Integration Tests: Run integration tests to ensure that all components of the service work together as expected.

Running Tests: Execute your tests using the following command:

```
docker-compose build
docker-compose run test
```
