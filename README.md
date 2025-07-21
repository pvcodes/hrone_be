# E-commerce Backend

Minimalist FastAPI backend for an e-commerce system with MongoDB.

## Project Structure

- `main.py`: Entry point, FastAPI app setup, CORS, health check.
- `routers/`:
  - `products.py`: Product CRUD (create, list with name/size filters).
  - `user.py`: User CRUD (create, list with name/email filters).
  - `orders.py`: Order create/list by user with product lookup.
- `models/`: Pydantic models (`Product`, `User`, `Order`).
- `db/main.py`: MongoDB connection/collections.
- `core/config.py`: Config (e.g., `ALLOWED_ORIGINS` for CORS).

## Setup

1. **Requirements**:

   - Python 3.8+
   - MongoDB
   - Install: `pip install fastapi uvicorn pymongo pydantic`

2. **Environment Variables**:

   - `DATABASE_URL`: Mongo Database URL
   - `HOST`: Server host (default: `0.0.0.0`).
   - `PORT`: Server port (default: `8080`).
   - `ALLOWED_ORIGINS`: CORS origins (comma-separated).

3. **Run**:
   ```bash
   uv run main.py
   ```
