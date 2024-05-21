# Forex Trading Platform API

Welcome to the Forex Trading Platform API! This API allows users to manage forex trading orders, providing endpoints to create, retrieve, and delete orders. It also supports real-time updates through WebSocket connections.

## Features

- Retrieve all orders
- Place a new order
- Retrieve a specific order
- Cancel an order
- Real-time order updates via WebSocket

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nikvrv/trading_task.git

# Run the application
- uvicorn src.main:app --host 0.0.0.0 --port 8000
- you also can start it with docker compose (tests are stored in another repos. Please check docker-compose)
- swagger is available on /api/openapi, however ws is not shown
