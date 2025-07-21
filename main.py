from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.main import connect_db, close_db, get_db_client
from routers import products, user, orders
from core.config import settings

app = FastAPI(title="Ecom BE")

# Include routers
app.include_router(products.router)
app.include_router(user.router)
app.include_router(orders.router)

# Event handlers
app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    db_client = await get_db_client()
    try:
        await db_client["ecommerce"].command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}


if __name__ == "__main__":
    import uvicorn

    if settings.ENV != "PRODUCTION":
        uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    else:
        uvicorn.run("main:app", workers=4, reload=False, log_level="info")
