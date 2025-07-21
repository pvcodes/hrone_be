from fastapi import APIRouter, Query, status
from db.main import get_db_and_collections
from typing import Dict, Any

from models.orders import Order

router = APIRouter(prefix="/orders")


@router.post("/")
async def create_order(order: Order, status_code=status.HTTP_201_CREATED):
    collections = await get_db_and_collections()
    order_collection = collections["order_collection"]
    result = await order_collection.insert_one(order.model_dump())
    return {"id": str(result.inserted_id)}


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def list_orders(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Dict[str, Any]:
    collections = await get_db_and_collections()
    order_collection = collections["order_collection"]

    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        {
            "$lookup": {
                "from": "product_collection",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "product_details",
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "items": {
                    "$map": {
                        "input": "$items",
                        "as": "item",
                        "in": {
                            "productDetails": {
                                "$arrayElemAt": [
                                    {
                                        "$filter": {
                                            "input": "$product_details",
                                            "as": "product",
                                            "cond": {
                                                "$eq": [
                                                    "$$product._id",
                                                    {"$toObjectId": "$$item.productId"},
                                                ]
                                            },
                                        }
                                    },
                                    0,
                                ]
                            },
                            "qty": "$$item.qty",
                        },
                    }
                },
                "_id": 0,
            }
        },
        {
            "$project": {
                "id": 1,
                "items": {
                    "productDetails": {
                        "id": {"$toString": "$items.productDetails._id"},
                        "name": "$items.productDetails.name",
                    },
                    "qty": 1,
                },
            }
        },
    ]

    total_count = await order_collection.count_documents({"userId": user_id})
    cursor = order_collection.aggregate(pipeline)

    data = [
        {
            "id": doc["id"],
            "items": [
                {
                    "productDetails": {
                        "id": item["productDetails"]["id"],
                        "name": item["productDetails"]["name"],
                    },
                    "qty": item["qty"],
                }
                for item in doc["items"]
            ],
        }
        async for doc in cursor
    ]

    return {
        "id": user_id,
        "data": data,
        "page": {
            "next": offset + limit if offset + limit < total_count else None,
            "previous": offset - limit if offset > 0 else None,
            "limit": limit,
        },
    }
