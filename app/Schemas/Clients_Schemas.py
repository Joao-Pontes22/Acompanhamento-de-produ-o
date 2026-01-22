from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class ClientsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    contact: str
    email: str
    phone: str

    @field_validator("name",
                     "contact", 
                     mode="before"
                     )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

    


class UpdateClientsInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("name",
                     "contact",
                      mode="before"
                      )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value