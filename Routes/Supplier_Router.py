from fastapi import APIRouter, Depends, HTTPException
from Dependecies import Init_Session, Verify_Token
from sqlalchemy.orm import Session
from models.Models import Suppliers, Employers
from Schemes.Supplier_Schemes import Suppliers_Scheme

Supplier_Router = APIRouter(prefix="/supplier", tags=["Supplier Operations"], dependencies=[Depends(Verify_Token)])
@Supplier_Router.post("/add_supplier")
async def add_supplier(scheme: Suppliers_Scheme,user_id: int = Depends(Verify_Token), session: Session = Depends(Init_Session)):
    employer_role = session.query(Employers).filter(Employers.ID == user_id).first()
    if employer_role.sector_ID != 2:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    supplier = Suppliers(name=scheme.supplier_name.upper(), contact=scheme.contact_name.upper(),
                         email=scheme.contact_email.lower(), phone=scheme.contact_phone)
    session.add(supplier)
    session.commit()
    return {"message": "Supplier added successfully", "supplier_name": supplier.name}

@Supplier_Router.get("/get_suppliers")
async def get_suppliers(session: Session = Depends(Init_Session)):
    suppliers = session.query(Suppliers).all()
    return suppliers