from pydantic import BaseModel, ConfigDict



class RelationMachinedXRaw_Scheme(BaseModel):
    raw_component_id: int
    machined_component_id: int
    qnty: int
    model_config = ConfigDict(from_attributes=True)