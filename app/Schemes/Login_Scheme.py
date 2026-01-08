from pydantic import BaseModel, ConfigDict

class Login_Scheme(BaseModel):
    emp_id: str
    password: str
    model_config = ConfigDict(from_attributes=True)