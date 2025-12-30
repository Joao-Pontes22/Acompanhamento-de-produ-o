from pydantic import BaseModel



class RelationMachinedXRaw_Scheme(BaseModel):
    raw_component_id: int
    machined_component_id: int
    qnty: int
    class config():
        from_attributes = True