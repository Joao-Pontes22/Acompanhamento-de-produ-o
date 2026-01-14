from app.models.Models import base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class Suppliers (base):
    __tablename__="Suppliers"

    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    contact = Column("contact", String)
    phone = Column("phone", String)
    email = Column("email", String)

    items = relationship("ComponentsAndParts", back_populates="supplier")
    stock = relationship("Stock", back_populates="suppliers")

    def __init__(self, name, contact, phone, email):
        self.name = name
        self.contact = contact
        self.phone = phone
        self.email = email