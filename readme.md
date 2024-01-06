# Train Ticketing Service

This is a simple train ticketing service implemented using gRPC in Python. The service allows users to purchase tickets, view their receipts, view users by section, remove users, and modify user seats.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You need to have Python 3.6 or later installed on your machine. You also need to install the following Python packages:

- grpcio
- grpcio-tools
- protobuf
- rich

You can install these packages using pip:

```bash
pip install grpcio grpcio-tools protobuf rich
```

### Running the Server

To start the server, navigate to the directory containing the `server.py` file and run the following command:

```bash
python server.py
```

The server will start and listen on port 50051.

### Running the Client

To start the client, navigate to the directory containing the `client.py` file and run the following command:

```bash
python client.py
```

The client will connect to the server and present a menu with the following options:

1. Purchase Ticket
2. Get Receipt
3. View Users By Section
4. Remove User
5. Modify User Seat
6. Exit

Follow the prompts to interact with the service.

## Running Tests

This project uses Python's built-in `unittest` framework for testing. To run the tests, navigate to the project's root directory and run the following command:

```bash
python -m unittest tests/test_server.py
```

This will discover and run all the test cases defined in the `test_server.py` file under the `tests` directory.

## Built With

- [Python](https://www.python.org/)
- [gRPC](https://grpc.io/)



