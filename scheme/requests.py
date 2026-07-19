from pydantic import BaseModel, TypeAdapter
from typing import List, Dict, Union, Literal
from uuid import UUID


class BaseRequest(BaseModel):
    collection_type: str
    collection_id: UUID

class NameRequest(BaseRequest):
    collection_type: Literal["name"]  
    p_name: str

class NumberRequest(BaseRequest):
    collection_type: Literal["pokemon_number"] 
    p_number: str
    
class RangeRequest(BaseRequest):
    collection_type: Literal["pokemon_range"]  
    p_range: str


RequestType =  Union[NameRequest, NumberRequest, RangeRequest]
request_adapter = TypeAdapter(RequestType)

def validate_request(request: dict) -> RequestType:
    return request_adapter.validate_python(request)


