from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from core.config import settings
from typing import Optional, Dict

db_client: Optional[AsyncIOMotorClient] = None


async def get_db_client() -> AsyncIOMotorClient:
    """Return database client instance."""
    return db_client


async def connect_db() -> None:
    """Create database connection."""
    global db_client
    db_client = AsyncIOMotorClient(settings.DATABASE_URL)
    print("DB Connected!")


async def close_db() -> None:
    """Close database connection."""
    db_client.close()


async def get_db_and_collections() -> Dict[str, AsyncIOMotorCollection]:
    """
    Initialize and return database and collections.

    Returns:
        Dict containing the database and individual collections.
    """
    client: AsyncIOMotorClient = await get_db_client()
    db: AsyncIOMotorDatabase = client.get_database("ecommerce")

    product_collection: AsyncIOMotorCollection = db.get_collection("products")
    user_collection: AsyncIOMotorCollection = db.get_collection("users")
    order_collection: AsyncIOMotorCollection = db.get_collection("orders")

    return {
        "db": db,
        "product_collection": product_collection,
        "user_collection": user_collection,
        "order_collection": order_collection,
    }
