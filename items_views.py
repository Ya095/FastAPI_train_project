from typing import Annotated
from fastapi import Path, APIRouter


router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}")
def get_item(item_id: Annotated[int, Path(ge=1, le=10_000)]):
    return {
        "item_id": item_id
    }


@router.get("/")
def list_items():
    return [
        "item1",
        "item2",
        "item3"
    ]
