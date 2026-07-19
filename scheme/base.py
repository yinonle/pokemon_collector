from pydantic import BaseMode, field 
from typing import List, Dict, Union, Literal
from uuid import UUID


class BaseCollectionRequest(BaseModel):
    collection_type: str
    collection_id: UUID

class NameCollectionName(BaseCollectionRequest):
    collection_type: Literal["name"]  
    p_name: str

class NameCollectionNumber(BaseCollectionRequest):
    collection_type: Literal["pokemon_number"] 
    p_number: str
    
class NameCollectionRange(BaseCollectionRequest):
    collection_type: Literal["pokemon_range"]  
    p_range: str