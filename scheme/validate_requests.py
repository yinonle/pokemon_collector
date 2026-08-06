from pydantic import BaseModel, TypeAdapter, model_validator, Field
from typing import Literal, Union, Optional, List, Dict, Any
from uuid import UUID


class NameCollectionRequest(BaseModel):
    collection_type: Literal["name"]
    collection_id: UUID
    p_name: str  

class NumberCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_number"]
    collection_id: UUID
    p_number: int = Field(ge=0, le=100)

class RangeCollectionRequest(BaseModel):
    collection_type: Literal["pokemon_range"]
    collection_id: UUID
    p_range: str    
    p_start: Optional[int] = None
    p_end: Optional[int] = None

    @model_validator(mode = "after")
    def parse_range(self) -> RangeCollectionRequest:
        try:
            parts = self.p_range.split("-")
            if len(parts) != 2:
                raise ValueError
            
            start, end = int(parts[0]), int(parts[1])
            if not (1 <= start <= 100 and 1 <= end <= 100 and start <= end):
                raise ValueError("Range out of bounds or start > end")
            
            self.p_start = start
            self.p_end = end
        except Exception:
            raise ValueError("Invalid format for p_range. Expected format: 'START-END' (e.g. '10-20').")
    
        return self

    
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


