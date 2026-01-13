from app.Schemes.Supplier_Schemes import Suppliers_Scheme, Suppliers_Scheme_Update
from app.domain.Entitys.Suppliers_entity import Suplliers_entity 
from app.domain.Value_objects import Supplier
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.domain.Value_objects.Supplier import value_Supplier
class Supplier_Services:
    def __init__(self, repo: Suppliers_Repositorie):
        self.repo = repo


    
    def service_create_supplier(self, scheme:Suppliers_Scheme):
        supplier = self.repo.repo_get_supplier_by_name(name=scheme.name)
        if supplier:
            raise AlreadyExist("Supplier")

        validated = Suplliers_entity(name=scheme.name,
                                     contact=scheme.contact,
                                     phone=scheme.phone,
                                     email=scheme.email)
                                     
        new_supplier = self.repo.repo_create_supplier(scheme=validated)
        return new_supplier
        
    def service_get_all_supplies(self):
        suppliers = self.repo.repo_get_all_suppliers()
        if not suppliers:
            raise NotFoundException("Suppliers")
        return  suppliers
    
    def service_get_supplier_by_name(self, name:str):
        supplier_entity = value_Supplier(supplier=name)
        supplier = self.repo.repo_get_supplier_by_name(name=supplier_entity.name)
        if not supplier:
            raise NotFoundException("Supplier")
        return supplier

    
    def service_update_supplier_info(self, supplier:str, scheme:Suppliers_Scheme_Update):
        supplier_entity = value_Supplier(supplier=supplier)
        supplier = self.repo.repo_get_supplier_by_name(name=supplier_entity.name)
        if not supplier:
            raise NotFoundException("Supplier")
        
        validated = Suplliers_entity(name=scheme.name,
                                     contact=scheme.contact,
                                     phone=scheme.phone,
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
    
    def service_delete_supplier(self, supplier:str):
        supplier_entity = value_Supplier(supplier=supplier)
        supplier = self.repo.repo_get_supplier_by_name(name=supplier_entity.name)
        if not supplier:
            raise NotFoundException("Supplier")
        deleted = self.repo.repo_delete_supplier(supplier=supplier)
        return deleted