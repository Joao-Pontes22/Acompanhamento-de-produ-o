from fastapi import  Depends
from sqlalchemy.orm import Session
from Models.Models import Stock
from Dependecies import Init_Session
from Schemes.Stock_Schemes import Stock_Scheme_warehouse

async def add_stock(scheme: Stock_Scheme_warehouse, session: Session =Depends(Init_Session)):
    new_stock = Stock(
        sector_ID=scheme.sector_ID,
        part_number=scheme.part_number.upper(),
        warehouse_batch=scheme.warehouse_batch.upper(),
        machining_batch=scheme.machining_batch.upper() if scheme.machining_batch else None,
        machining_date=scheme.machining_date if scheme.machining_date else None,
        qnty=scheme.qnty,
        entry_date_warehouse_batch=scheme.entry_date_warehouse_batch,
        supplier_ID=scheme.supplier_ID,
        status=scheme.status.upper(),
        cost=scheme.cost
    )
    session.add(new_stock)
    session.commit()
    session.refresh(new_stock)
    return {"message": "Stock added successfully", "stock": new_stock}