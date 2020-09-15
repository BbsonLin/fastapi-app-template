from typing import Optional

from fastapi import APIRouter

api_router = APIRouter()


fake_items_db = [{"id": 1, "item_name": "Foo"}, {"id": 2, "item_name": "Bar"},
                 {"id": 3, "item_name": "Baz"}]


@api_router.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@api_router.get("/items/{item_id}")
async def read_item_by_id(item_id: int, q: Optional[str] = None):
    fake_items_db
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
