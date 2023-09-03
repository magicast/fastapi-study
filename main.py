"""study fastapi"""

from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Query, Path


app = FastAPI()


class Item(BaseModel):
    """item class"""
    name: str
    price: float
    is_offer: Annotated[bool | None, "is_offer parameter"] = None


@app.get("/")
def read_root():
    """root page"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[str, Path(title='item id', description='item id', min_length=4)],
    quantity: Annotated[int | None, Query(
        title='quantity',
        description='must greater than equal 1', alias='q', ge=1)] = None,
    short: Annotated[bool, Query(title='short')] = False):
    """read item page"""
    item = {"item_id": item_id}
    if quantity:
        item.update({"q": quantity})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """update item page"""
    return {"item_name": item.name, "item_id": item_id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """read items. paging"""
    return fake_items_db[skip : skip + limit]

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, quantity: str | None = None, short: bool = False,
    ):
    """read user item page. path and optional querystring"""
    item = {"item_id": item_id, "owner_id": user_id}
    if quantity:
        item.update({"quantity": quantity})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# @app.get("/items/{item_id}")
# async def read_user_item_2(item_id: str, needy: str):
#     """read user item. required querystring"""
#     item = {"item_id": item_id, "needy": needy}
#     return item
