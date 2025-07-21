from fastapi import APIRouter, Query, status
from models.products import Product
from db.main import get_db_and_collections
from typing import Optional, Dict, Any
import re

router = APIRouter(prefix="/products")


@router.post("/")
async def create_product(product: Product, status_code=status.HTTP_201_CREATED):
    collections = await get_db_and_collections()
    result = await collections["product_collection"].insert_one(product.model_dump())
    return {"id": str(result.inserted_id)}


@router.get("/")
async def list_products(
    name: Optional[str] = Query(None, description="Search by partial name"),
    size: Optional[str] = Query(None, description="Filter by size"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_code=status.HTTP_200_OK,
) -> Dict[str, Any]:
    collections = await get_db_and_collections()
    product_collection = collections["product_collection"]

    filters = {}
    if name:
        filters["name"] = {"$regex": re.escape(name), "$options": "i"}
    if size:
        filters["size"] = size

    pipeline = [
        {"$match": filters},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        {"$project": {"id": {"$toString": "$_id"}, "name": 1, "price": 1, "_id": 0}},
    ]

    total_count = await product_collection.count_documents(filters)
    cursor = product_collection.aggregate(pipeline)

    data = [
        {"id": doc["id"], "name": doc["name"], "price": doc.get("price")}
        async for doc in cursor
    ]

    return {
        "data": data,
        "page": {
            "next": offset + limit if offset + limit < total_count else None,
            "previous": offset - limit if offset > 0 else None,
            "limit": limit,
        },
    }
