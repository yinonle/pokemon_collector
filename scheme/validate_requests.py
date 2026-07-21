from pydantic import BaseModel, TypeAdapter, Field
from typing import Literal, Union
from uuid import UUID


class NameCollectionRequest(BaseModel):
    collection_type: Literal["name"]
    collection_id: UUID
    p_name: str  

class NumberCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_number"]
    collection_id: UUID
    p_number: str  

class RangeCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_range"]
    collection_id: UUID
    p_range: str  

SqsMessage = Union[NameCollectionRequest, NumberCollectionRequest, RangeCollectionRequest]
sqs_adapter = TypeAdapter(SqsMessage)
#sqs_message = SqsMessage(p_name=[""])


#sqs_message
#‹