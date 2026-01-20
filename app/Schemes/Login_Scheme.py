from pydantic import BaseModel, ConfigDict, field_validator

class LoginScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    emp_id: str
    password: str

    @field_validator("emp_id", mode="before")

    @classmethod
    def to_upper(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

    