from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session, Verify_Token
from sqlalchemy.orm import Session
from app.Schemes.Supplier_Schemes import Suppliers_Scheme, Suppliers_Scheme_Update
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.Services.Supplier_Services import Supplier_Services
Supplier_Router = APIRouter(prefix="/supplier", tags=["Supplier Operations"])
@Supplier_Router.post("/add_supplier")
async def add_supplier(scheme: Suppliers_Scheme,session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    new_supplier = service.service_create_supplier(scheme=scheme)
    return {"message": "New supplier added successfuly",
            "Supplier": new_supplier.name}

@Supplier_Router.get("/get_suppliers")
async def get_suppliers(session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    suppliers = service.service_get_all_supplies()
    return suppliers

@Supplier_Router.get("/get_supplier/{supplier_id}")
async def get_supplier(supplier_id: int, session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    supplier = service.service_get_supplier_by_id(supplier_id)
    return supplier

@Supplier_Router.patch("/Updated_supplie_info")
async def update_supplier(id:int, scheme:Suppliers_Scheme_Update, session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    supplier = service.service_update_supplier_info(id=id,scheme=scheme)
    return {"message": "Supplie updated successfuly",
            "Supplier": supplier}

@Supplier_Router.delete("/Delete_Supplier")
async def delete_supplier(id:int, session:Session=Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    supplier = service.service_delete_supplier(id=id)
    return {"message": "Supplier deleted successfully",
            "Supplier": supplier}