from typing import Union
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.tools import parse_obj_as
import property.Class
from property.Class import Property

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q":q}

@app.get("/properties")
def get_properties():
    properties = new Property()
    with open("mocks/data/properties-landing-assets.json", "r+") as file:
        d = json.read(file)
        
    return FileResponse("mocks/data/properties-landing-assets.json")

        