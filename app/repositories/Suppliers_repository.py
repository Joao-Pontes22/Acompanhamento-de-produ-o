
from app.models.Suppliers import Suppliers

class SuppliersRepository:
    def __init__(self, session):
        self.session = session
    


    def create_supplier(self,
                             name: str,
                             contact: str,
                             phone: str,
                             email: str
                             ):
        new_supplier = Suppliers(name=name,
                                 contact=contact,
                                 phone=phone,
                                 email=email
                                 )
        self.session.add(new_supplier)
        self.session.commit()
        return new_supplier
    

    def get_all_suppliers(self):
        suppliers = self.session.query(Suppliers).all()
        return suppliers
    

    def get_supplier_by_id(self, id:int):
        supplier = self.session.query(Suppliers).filter(Suppliers.ID == id).first()
        return supplier
    
    def get_supplier_by_name(self, name:str):
        supplier = self.session.query(Suppliers).filter(Suppliers.name == name).first()
        return supplier
    

    def delete_supplier(self, supplier):
        self.session.delete(supplier)
        self.session.commit()
        return supplier
    
    def update_suppliers_info(self, supplier):
        self.session.commit()
        self.session.refresh(supplier)
        return supplier