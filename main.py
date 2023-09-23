from typing import Union
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic.tools import parse_obj_as
from models.property import *
import os,json
from typing import List

from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def app_startup():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
        
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q":q}

# @app.get("/properties")
# def get_properties():
#     return fake_db["properties"]

# @app.get("/property/{id}")
# def get_property(id):
#     return search(id, fake_db["properties"])