# Transection Service
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

## 5. swagger UI link 
Here is swagger link : http://0.0.0.0:8000/docs

## 6 . Stopping the Server
To stop the running Docker containers, use:


```console
docker-compose down
```

## 7. API that we support 
PUT
/transactionservice/transaction/{transaction_id}
Create Transaction


GET
/transactionservice/transaction/{transaction_id}
Get Transaction By Id

GET
/transactionservice/types/{transaction_type}
Get Transactions By Type

GET
/transactionservice/sum/{transaction_id}
Get Transaction Sum
