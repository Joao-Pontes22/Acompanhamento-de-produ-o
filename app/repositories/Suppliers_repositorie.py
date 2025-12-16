from app.Schemes.Supplier_Schemes import  Suppliers_Scheme
from app.models.Models import Suppliers

class Suppliers_Repositorie:
    def __init__(self, session):
        self.session = session
    


    def repo_create_supplier(self, scheme:Suppliers_Scheme):
        new_supplier = Suppliers(name=scheme.name,
                                 contact=scheme.contact,
                                 phone=scheme.phone,
                                 email=scheme.email)
        self.session.add(new_supplier)
        self.session.commit()
        return new_supplier
    

    def repo_get_all_suppliers(self):
        suppliers = self.session.query(Suppliers).all()
        return suppliers
    

    def repo_get_suplier_by_id(self, id:int):
        supplier = self.session.query(Suppliers).filter(Suppliers.ID == id).first()
        return supplier
    
    def repo_get_supplier_by_name(self, name:str):
        supplier = self.session.query(Suppliers).filter(Suppliers.ID == name).first()
        return supplier
    

    def repo_delete_supplier(self, supplier:Suppliers_Repositorie):
        self.session.delete(supplier)
        self.session.commit()
        return supplier
    
    def repo_update_suppliers_info(self, supplier:Suppliers_Repositorie):
        self.session.commit()
        self.session.refresh(supplier)
        return supplier