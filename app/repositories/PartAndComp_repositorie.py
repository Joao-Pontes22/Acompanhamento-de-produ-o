from app.models.ComponentsAndParts import ComponentsAndParts
from sqlalchemy.orm import Session


class PartsAndComp_Repositorie:
    def __init__(self, session: Session):
        self.session = session

    def repo_get_Parts_and_Components_by_part_number(self, part_number: str):
        return self.session.query(ComponentsAndParts).filter(ComponentsAndParts.part_number == part_number).first()