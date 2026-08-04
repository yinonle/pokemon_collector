from pydantic import BaseModel, TypeAdapter, field_validator, Field
from typing import Literal, Union, Optional, List, Dict, Any
from uuid import UUID


class NameCollectionRequest(BaseModel):
    collection_type: Literal["name"]
    collection_id: UUID
    p_name: str  

class NumberCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_number"]
    collection_id: UUID
    p_number: int 

class RangeCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_range"]
    collection_id: UUID
    p_range: str 
    
    @field_validator("p_range")
    @classmethod
    def parse_num_range(cls, pok_range: str) -> str:
        try:
            parts = pok_range.split("-")
            
            start, end = int(parts[0]), int(parts[1])
            if start > end:
                raise ValueError("pokemon_range not optimize")

        except Exception:
            raise ValueError("Your input format not valid please folow this format: START-END")

    
        return pok_range


SqsMessage = NameCollectionRequest | NumberCollectionRequest | RangeCollectionRequest
sqs_adapter = TypeAdapter(SqsMessage)

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

class ProcessResult(BaseModel):
    valid: bool
    data: Optional[CollectorOutputResponse] = None
    error: Optional[str] = None


