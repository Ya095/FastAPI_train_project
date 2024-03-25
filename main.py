from fastapi import FastAPI, Body
import uvicorn
from pydantic import EmailStr


app = FastAPI(title="Magic API", version="1.0.0", description="Testing API of FastAPI :)")


@app.get("/")
def hello_world():
    return {
        "message": "Hello World"
    }


@app.get("/hello")
def hello(name: str):
    name = name.strip().title()
    return {
        "message": f"Hello {name}"
    }


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id
    }


@app.post("/users")
def create_user(email: EmailStr = Body()):
    return {
        "message": "Success",
        "email": email
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
