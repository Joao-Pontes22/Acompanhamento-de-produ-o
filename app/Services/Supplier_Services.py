from app.Schemes.Supplier_Schemes import Suppliers_Scheme, Suppliers_Scheme_Update
from app.domain.Entitys.Suppliers_entity import Suplliers_entity 
from fastapi import HTTPException
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
class Supplier_Services:
    def __init__(self, repo: Suppliers_Repositorie):
        self.repo = repo


    
    def service_create_supplier(self, scheme:Suppliers_Scheme):
        supplier = self.repo.repo_get_supplier_by_name(name=scheme.name)
        if supplier:
            raise HTTPException(status_code=400, detail="Supplier aleady exist")

        validated = Suplliers_entity(name=scheme.name,
                                     contact=scheme.contact,
                                     phone=scheme.contact,
                                     email=scheme.email)
                                     
        new_supplier = self.repo.repo_create_supplier(scheme=validated)
        return new_supplier
        
    def service_get_all_supplies(self):
        suppliers = self.repo.repo_get_all_suppliers()
        if not suppliers:
            raise HTTPException(status_code=400, detail="suppliers not exist yet")
        return  suppliers
    
    def service_get_supplier_by_id(self, id:int):
        supplier = self.repo.repo_get_suplier_by_id(id=id)
        if not supplier:
            raise HTTPException(status_code=400, detail="supplier not found")
        return supplier
    
    def sevice_get_supplier_by_name(self, name:str):
        supplier = self.repo.repo_get_supplier_by_name(name=name)
        if not supplier:
            raise HTTPException(status_code=400, detail="supplier not found")
        return supplier
    
    def service_update_supplier_info(self, id:int, scheme:Suppliers_Scheme_Update):
        supplier = self.repo.repo_get_suplier_by_id(id=id)
        if not supplier:
            raise HTTPException(status_code=400, detail="supplier not found")
        
        validated = Suplliers_entity(name=scheme.name,
                                     contact=scheme.contact,
                                     phone=scheme.contact,
                                     email=scheme.email)
        if scheme.name is not None:
            supplier.name = validated.name
        if scheme.contact is not None:
            supplier.contact = validated.contact
        if scheme.phone is not None:
            supplier.phone = validated.phone
        if scheme.email is not None:
            supplier.email = validated.email
        new_supplier_infos = self.repo.repo_update_suppliers_info(supplier=supplier)
        return new_supplier_infos
    
    def service_delete_supplier(self, id:int):
        supplier = self.repo.repo_get_suplier_by_id(id=id)
        if not supplier:
            raise HTTPException(status_code=400, detail="supplier not found")
        deleted = self.repo.repo_delete_supplier(supplier=supplier)
        return deleted