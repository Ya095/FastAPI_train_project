from fastapi import FastAPI, Body
import uvicorn
from pydantic import EmailStr
from items_views import router as items_router
from users.views import router as users_router


app = FastAPI(title="Magic API", version="1.0.0", description="Testing API of FastAPI :)")
app.include_router(items_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
