# Transaction Service
We would like to have a RESTful web service that stores some transactions (in memory is fine) and
returns information about those transactions. The transactions to be stored have a type and an
amount. The service should support returning all transactions of a type. Also, transactions can be
linked to each other (using a ”parent id”) and we need to know the total amount involved for all
transactions linked to a particular transaction.

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

Endpoint: PUT /transactionservice/transactions/{transection_id}

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
```

8.2. Test Case: Retrieve Transactions by Types
Description: Ensure that transactions can be retrieved based on their type.
```
Endpoint: GET /transactionservice/types/{transaction_type}
```
Example Request:
```
curl -X GET "http://localhost:8000//transactionservice/types/expense"
Expected Response:


Status Code: 200 OK
Response Body: (List of transactions with the specified type)
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
```


8.4. Test Case: get total transection value -- parent child 
Description: Verify that the total amount for all transactions linked to a specific transaction is calculated correctly.


Endpoint: GET GET /transactionservice/sum/{transaction_id}

Example Request:
```
curl -X GET "http://localhost:8000/GET /transactionservice/sum/1"
Expected Response:

Status Code: 200 OK
Response Body: {"sum": 100} 
```


## 9 Running Tests
## Unit Tests: Ensure your unit tests are written to cover the functionality of the service. You can use testing frameworks like pytest for Python.

Integration Tests: Run integration tests to ensure that all components of the service work together as expected.

Running Tests: Execute your tests using the following command:

```
docker-compose build
docker-compose run test
```
