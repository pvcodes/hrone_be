from fastapi import APIRouter, status
from db.main import get_db_and_collections
from models.users import User

router = APIRouter(prefix="/users")


@router.post("/")
async def create_user(user: User, status_code=status.HTTP_201_CREATED):
    collections = await get_db_and_collections()
    user_collection = collections["user_collection"]
    # TODO: password can be hashed for better security
    result = await user_collection.insert_one(user.model_dump())
    return {"id": str(result.inserted_id)}
