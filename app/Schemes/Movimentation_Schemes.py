from pydantic import BaseModel, ConfigDict

class MovimentationScheme(BaseModel):
    part_number: str
    origin: str
    reason: str
    movimentation_type: str
    employer_id: int
    batch: str = None
    qnty: int
    date: str
    destination: str
    machining_batch: str | None = None
    assembly_batch: str | None = None
    model_config = ConfigDict(from_attributes=True)