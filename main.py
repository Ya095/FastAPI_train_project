from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from core.models import Base, db_helper
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up the ML models and release the resources


app = FastAPI(
    lifespan=lifespan,
    title="Magic API",
    version="1.0.0",
    description="Testing API of FastAPI :)"
)
app.include_router(items_router)
app.include_router(users_router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
