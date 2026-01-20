from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class ClientsScheme(BaseModel):
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
    

    


class UpdateClientsInfoScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str]
    contact: Optional[str]
    email: Optional[str] 
    phone: Optional[str] 

    @field_validator("name",
                     "contact",
                      mode="before"
                      )
    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value