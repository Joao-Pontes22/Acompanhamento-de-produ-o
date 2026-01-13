from pydantic import BaseModel, ConfigDict
class Relation_Scheme(BaseModel):
    create_item_part_number: str
    consume_item_part_number: str
    qnty: int
    model_config = ConfigDict(from_attributes=True)


class Relation_Scheme_Update(BaseModel):
    create_item_part_number: str | None = None
    consume_item_part_number: str | None = None
    qnty: int | None = None
    model_config = ConfigDict(from_attributes=True)