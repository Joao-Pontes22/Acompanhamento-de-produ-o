#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session, Verify_Token
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas
from app.Schemas.Supplier_Schemas import SuppliersSchema, UpdateSupplierInfosSchema
#Repository
from app.repositories.Suppliers_repository import SuppliersRepository
#Service
from app.Services.Supplier_Service import SupplierService
#Exceptions
from app.domain.Exceptions import NotFoundException, AlreadyExist



Supplier_Router = APIRouter(prefix="/supplier", tags=["Supplier Operations"])


@Supplier_Router.post("/add_supplier")
async def add_supplier(body: SuppliersSchema,
                       session: Session = Depends(Init_Session)):
    
    repo = SuppliersRepository(session=session)
    service = SupplierService(repo=repo)

    try:

        new_supplier = service.create_supplier(scheme=body)

        return {"message": "New supplier added successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@Supplier_Router.get("/get_suppliers")
async def get_suppliers(session: Session = Depends(Init_Session)):

    repo = SuppliersRepository(session=session)
    service = SupplierService(repo=repo)
    try:

        suppliers = service.get_all_supplies()

        return suppliers
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.get("/get_supplier/{supplier}")
async def get_supplier(supplier: str, 
                       session: Session = Depends(Init_Session)
                       ):
    repo = SuppliersRepository(session=session)
    service = SupplierService(repo=repo)

    try:

        supplier = service.get_supplier_by_name(supplier)

        return supplier
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.patch("/updated_supplier_info/{supplier}")
async def update_supplier(supplier:str, 
                          body:UpdateSupplierInfosSchema, 
                          session: Session = Depends(Init_Session)):
    repo = SuppliersRepository(session=session)
    service = SupplierService(repo=repo)

    try:
        supplier = service.update_supplier_info(supplier=supplier,scheme=body)

        return {"message": "Supplie updated successfuly",
                "Supplier": supplier}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Supplier_Router.delete("/delete_supplier/{supplier}")
async def delete_supplier(supplier:str, 
                          session:Session=Depends(Init_Session)
                          ):

    repo = SuppliersRepository(session=session)
    service = SupplierService(repo=repo)

    try:
        supplier = service.delete_supplier(supplier=supplier)

        return {"message": "Supplier deleted successfully",
                "Supplier": supplier}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))