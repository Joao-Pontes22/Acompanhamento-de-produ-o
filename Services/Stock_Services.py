from fastapi import  Depends
from sqlalchemy.orm import Session
from models.Models import Stock, componentsAndparts
from Dependecies import Init_Session
from Schemes.Stock_Schemes import Stock_Scheme_warehouse

async def add_stock(scheme: Stock_Scheme_warehouse, session: Session =Depends(Init_Session)):
    lastwarehousebatch = session.query(Stock).order_by(Stock.ID.desc()).first()
    if not lastwarehousebatch:
        warehousebatch = 0
    data = session.query(componentsAndparts).filter(componentsAndparts.part_number == scheme.part_number.upper()).first()
    new_stock = Stock(
        sector_ID=scheme.sector_ID,
        part_number=scheme.part_number.upper(),
        warehouse_batch=warehousebatch + 1,
        machining_batch=None,
        machining_date=None,
        qnty=scheme.qnty,
        entry_date_warehouse_batch=scheme.entry_date_warehouse_batch,
        supplier_ID=scheme.supplier_ID,
        status="DISPONIVEL",
        cost=data.cost * scheme.qnty
        )
    session.add(new_stock)
    session.commit()
    session.refresh(new_stock)
    return {"message": "Stock added successfully", "stock": new_stock}

async def get_all_stock(session: Session = Depends(Init_Session)):
    stocks = session.query(Stock).all()
    return stocks