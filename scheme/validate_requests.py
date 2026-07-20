from pydantic import BaseModel, TypeAdapter, model_validator
from typing import List, Dict, Union, Literal, Optional
from uuid import UUID


class SqsMessage(BaseModel):
    collection_type: Literal["name", "pokemon_number", "pokemon_range"]
    collection_id: UUID

    p_name: Optional[str] = None
    p_number: Optional[str] = None
    p_range: Optional[str] = None

    @model_validator(mode="after")
    def validate_fields_by_type(self):
        if self.collection_type == "name" and not self.p_name:
            raise ValueError("p_name must be provided when collection_type is 'name'")
        elif self.collection_type == "pokemon_number" and not self.p_number:
            raise ValueError("p_number must be provided when collection_type is 'pokemon_number'")
        elif self.collection_type == "pokemon_range" and not self.p_range:
            raise ValueError("p_range must be provided when collection_type is 'pokemon_range'")
        return self

#sqs_message = SqsMessage(p_name=[""])


#sqs_message