from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Clients (base):
    __tablename__="Clients"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    contact = Column("contact", String)
    phone = Column("phone", String)
    email = Column("email", String)

    stock = relationship("Stock", back_populates="clients")
    items = relationship("ComponentsAndParts",  back_populates="clients")
    def __init__(self, name, contact, phone, email):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.email = email
