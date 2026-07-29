from pydantic import BaseModel, TypeAdapter, field_validator, Field
from typing import Literal, Union, List, Dict, Any
from uuid import UUID


class NameCollectionRequest(BaseModel):
    collection_type: Literal["name"]
    collection_id: UUID
    p_name: str  

class NumberCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_number"]
    collection_id: UUID
    p_number: int # = Field(gt=0, lt=101) 

    
    # @field_validator("p_number")
    #@classmethod
    ##   if not (1 <= num_in_range <=100):
      #      raise ValueError(f"Pokemon number {num_in_range} is out from the allowd range: 1 - 100")
       # return num_in_range
    

class RangeCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_range"]
    collection_id: UUID
    p_range: str  

    @field_validator("p_range")
    @classmethod
    def parse_num_range(cls, pok_range: str) -> str:
        try:
            parts = pok_range.split("-")
            if len(parts) != 2:
                raise ValueError
            
            start, end = int(parts[0]), int(parts[1])

        except Exception:
            raise ValueError("Your input format not valid please folow this format: START-END ")

        if start > end:
            raise ValueError("pokemon_range not optimize!")
    
        return pok_range

#TODO export the parse of range
SqsMessage = Union[NameCollectionRequest, NumberCollectionRequest, RangeCollectionRequest]
sqs_adapter = TypeAdapter(SqsMessage)

#sqs_message = SqsMessage(p_name=[""])
#sqs_message
#‹

class PokemonModel(BaseModel):
    serial_number: int = Field(gt=0, lt=101)
    name: str
    type: str
    weight: str
    height: str
    evolution_links: List[str]


class CollectorOutputResponse(BaseModel):
    collection_id: UUID
    pokelist: List[PokemonModel]
    failed_list: List[str]


