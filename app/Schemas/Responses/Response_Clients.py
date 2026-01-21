from pydantic import BaseModel,ConfigDict



class ResponseClients(BaseModel):
    name: str
    contact: str
    email: str
    phone: str
    model_config = ConfigDict(from_attributes=True)