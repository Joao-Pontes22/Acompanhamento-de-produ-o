from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Relation (base):
    __tablename__="Relation"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    create_item_Part_number = Column("create_item_Part_number", Integer)
    consume_item_Part_number = Column("consume_item_Part_number", Integer)
    qnty = Column("qnty", Integer)
   
    def __init__(self, create_item_Part_number, consume_item_Part_number, qnty):
        self.create_item_Part_number = create_item_Part_number
        self.consume_item_Part_number = consume_item_Part_number
        self.qnty = qnty