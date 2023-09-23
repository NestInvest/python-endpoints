from typing import List
from pydantic import BaseModel

class Location(BaseModel):
    address: str
    city: str
    state: str
    zipcode: str
    country: str

class Contact(BaseModel):
    agentName: str
    agentPhone: str
    agentEmail: str
    
class Property(BaseModel):
    propertyId: str
    propertyName: str
    propertyType: str
    price: str
    bedrooms: int
    bathrooms: int
    area: str
    location: Location
    description: str
    features: List[str]
    images: List[str]
    contact: Contact

    