from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.property import *

router = APIRouter()

@router.post("/", response_description="Create a new property", status_code=status.HTTP_201_CREATED, response_model=Property)
def create_property(request: Request, property: Property = Body(...)):
    property = jsonable_encoder(property)
    new_property = request.app.database["properties"].insert_one(property)
    created_property = request.app.database["properties"].find_one(
        {"_id": new_property.inserted_id}
    )

    return created_property

@router.get("/", response_description="List all properties", response_model=List[Property])
def list_properties(request: Request):
    properties = list(request.app.database["properties"].find(limit=100))
    return properties

@router.get("/{id}", response_description="Get a single property by id", response_model=Property)
def find_property(id: str, request: Request):
    if (property := request.app.database["properties"].find_one({"_id": id})) is not None:
        return property
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

@router.put("/{id}", response_description="Update a property", response_model=Property)
def update_property(id: str, request: Request, property: Property = Body(...)):
    property = {k: v for k, v in property.dict().items() if v is not None}
    if len(property) >= 1:
        update_result = request.app.database["properties"].update_one(
            {"_id": id}, {"$set": property}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

    if (
        existing_property := request.app.database["properties"].find_one({"_id": id})
    ) is not None:
        return existing_property

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {id} not found")

@router.delete("/{id}", response_description="Delete a property")
def delete_property(id: str, request: Request, response: Response):
    delete_result = request.app.database["properties"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Properties with ID {id} not found")