from typing import Union
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.tools import parse_obj_as
from models.property import *
import os,json
from typing import List
import pymongo

fake_db = {
    "properties": List[Property],
    "property": Property
}
path_to_json = '/mocks/data/property-details/'


app = FastAPI()

def search(id, test_list):
    return [element for element in test_list if element['propertyId'] == id]
 

@app.on_event("startup")
def app_startup():
    with open("mocks/data/properties-landing-assets.json", "r+") as file:
        data = json.load(file)
        properties = parse_obj_as(List[Property], data)   
        fake_db["properties"] = properties
        
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q":q}

@app.get("/properties")
def get_properties():
    return fake_db["properties"]

@app.get("/property/{id}")
def get_property(id):
    return search(id, fake_db["properties"])