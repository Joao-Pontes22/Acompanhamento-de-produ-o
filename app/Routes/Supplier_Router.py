from fastapi import APIRouter, Depends, HTTPException
from app.core.Dependecies import Init_Session, Verify_Token
from sqlalchemy.orm import Session
from app.Schemes.Supplier_Schemes import Suppliers_Scheme, Suppliers_Scheme_Update
from app.repositories.Suppliers_repositorie import Suppliers_Repositorie
from app.Services.Supplier_Services import Supplier_Services
from app.domain.Exceptions import NotFoundException, AlreadyExist
Supplier_Router = APIRouter(prefix="/supplier", tags=["Supplier Operations"])
@Supplier_Router.post("/add_supplier")
async def add_supplier(scheme: Suppliers_Scheme,session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    try:
        new_supplier = service.service_create_supplier(scheme=scheme)
        return {"message": "New supplier added successfuly",
                "Supplier": new_supplier.name}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@Supplier_Router.get("/get_suppliers")
async def get_suppliers(session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    try:
        suppliers = service.service_get_all_supplies()
        return suppliers
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.get("/get_supplier/{supplier}")
async def get_supplier(supplier: str, session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    try:
        supplier = service.service_get_supplier_by_name(supplier)
        return supplier
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.patch("/updated_supplier_info/{supplier}")
async def update_supplier(supplier:str, scheme:Suppliers_Scheme_Update, session: Session = Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    try:
        supplier = service.service_update_supplier_info(supplier=supplier,scheme=scheme)
        return {"message": "Supplie updated successfuly",
                "Supplier": supplier}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.delete("/delete_supplier/{supplier}")
async def delete_supplier(supplier:str, session:Session=Depends(Init_Session)):
    repo = Suppliers_Repositorie(session=session)
    service = Supplier_Services(repo=repo)
    try:
        supplier = service.service_delete_supplier(supplier=supplier)
        return {"message": "Supplier deleted successfully",
                "Supplier": supplier}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))