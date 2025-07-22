# E-commerce Backend

Minimalist FastAPI backend for an e-commerce system with MongoDB. [click here,  must read](#what-else-can-be-done)

### Keep in mind while evaluating the code

- To test the endpoint, first send a GET request to https://hrone-be-221t.onrender.com/. Since it's deployed on Render's free tier, it may take a moment to start. Wait for this response:
  ```
  {
  "status": "healthy",
  "database": "connected"
  }
  ```
  Once received, proceed with your test script.

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

   - Python 3.8+ and `uv` package
   - MongoDB
   - Install: `uv pip install -r pyproject.toml`

2. **Environment Variables**:

   - `DATABASE_URL`: Mongo Database URL
   - `HOST`: Server host (default: `0.0.0.0`).
   - `PORT`: Server port (default: `8080`).
   - `ALLOWED_ORIGINS`: CORS origins (comma-separated).

3. **Run**:
   ```bash
   uv run main.py
   ```

## What else can be done?

1. **Introduce middleware for authentication and authorization**:

   - Implement JWT-based authentication to secure endpoints.
   - Add role-based authorization (e.g., admin, user) to restrict access to specific routes like `/products` or `/orders`.
   - Use FastAPI's `Depends` with OAuth2 or custom middleware to validate tokens and user permissions.

2. **Rate limiting**:

   - Implement rate-limiting middleware (e.g., `slowapi`) to prevent abuse and ensure fair usage of API endpoints.

3. **Error handling**:

   - Create custom exception handlers for consistent error responses (e.g., 400, 404, 500).
   - Log errors to a file or service (e.g., Sentry) for monitoring and debugging.

4. **Caching**:
   - Use in-memory caching (e.g., Redis) for frequently accessed data like product listings to reduce database load.
   - Implement cache-control headers for GET endpoints.
