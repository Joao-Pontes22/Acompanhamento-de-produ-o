#Schema
from app.Schemas.Supplier_Schemas import SuppliersSchema, UpdateSupplierInfosSchema
#Entity
from app.domain.Entitys.Suppliers_entity import SuplliersEntity
#Repository
from app.repositories.Suppliers_repository import SuppliersRepository
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist
#Value Object
from app.domain.Value_objects.Supplier import value_Supplier

class SupplierService:
    def __init__(self, repo: SuppliersRepository):
        self.repo = repo


    
    def create_supplier(self, scheme:SuppliersSchema):
    
        supplier = self.repo.get_supplier_by_name(name=scheme.name)
        if supplier:
            raise AlreadyExist("Supplier")

        entity = SuplliersEntity(name=scheme.name,
                                 contact=scheme.contact,
                                 phone=scheme.phone,
                                 email=scheme.email)
                                     
        new_supplier = self.repo.create_supplier(name=entity.supplier_name,
                                                 contact=entity.contact,
                                                 phone=entity.phone,
                                                 email=entity.email
                                                 )
        return new_supplier
        
    def get_all_supplies(self):

        suppliers = self.repo.get_all_suppliers()
        if not suppliers:
            raise NotFoundException("Suppliers")
        
        return  suppliers
    
    def get_supplier_by_name(self, name:str):
        
        value_supplier = value_Supplier(supplier=name)
        supplier = self.repo.get_supplier_by_name(name=value_supplier.name)
        if not supplier:
            raise NotFoundException("Supplier")
        
        return supplier

    
    def update_supplier_info(self, supplier:str, schema:UpdateSupplierInfosSchema):

        value_supplier = value_Supplier(supplier=supplier)
        supplier = self.repo.get_supplier_by_name(name=value_supplier.name)
        if not supplier:
            raise NotFoundException("Supplier")
        
        entity = SuplliersEntity(name=schema.name,
                                     contact=schema.contact,
                                     phone=schema.phone,
                                     email=schema.email)
        
        for field, value in schema.model_dump(exclude_unset=True):
            setattr(supplier, field, value)

        new_supplier_infos = self.repo.update_suppliers_info(supplier=supplier)

        return new_supplier_infos
    
    def delete_supplier(self, supplier:str):

        supplier = self.repo.get_supplier_by_name(name=supplier)
        if not supplier:
            raise NotFoundException("Supplier")
        
        deleted = self.repo.delete_supplier(supplier=supplier)

        return deleted
    