from app.domain.Entitys.Stock_entitys import Stock_Entity
from app.models.Stock import Stock
from app.Schemes.Stock_Schemes import Stock_Scheme_models
class Stock_repositorie:
    def __init__(self, session):
        self.session = session
        pass 

    

    def create_stock(self,scheme: Stock_Scheme_models):
        new_stock = Stock(sector_name=scheme.sector_name,
                          part_number=scheme.part_number,
                          batch=scheme.batch,
                          machining_batch=scheme.machining_batch,
                          machining_date=scheme.machining_date,
                          assembly_batch=scheme.assembly_batch,
                          assembly_date=scheme.assembly_date,
                          qnty=scheme.qnty,
                          entry_date=scheme.entry_date, 
                          supplier_ID=scheme.supplier_ID, 
                          status=scheme.status, 
                          cost=scheme.cost,
                          client_ID=scheme.client_ID
                          )
        self.session.add(new_stock)
        self.session.commit()
        return new_stock
    

    def create_stock(self,scheme: Stock_Entity):
        new_stock = Stock(sector_name=scheme.sector_name,
                          part_number=scheme.part_number,
                          batch=scheme.batch,
                          machining_batch=scheme.machining_batch,
                          machining_date=scheme.machining_date,
                          assembly_batch=scheme.assembly_batch,
                          assembly_date=scheme.assembly_date,
                          qnty=scheme.qnty,
                          entry_date=scheme.entry_date, 
                          supplier_name=scheme.supplier_name, 
                          status="ACTIVE", 
                          cost=scheme.cost,
                          client_name=scheme.client_name
                          )
        self.session.add(new_stock)
        self.session.commit()
        return new_stock

   
    def get_all_stock(self):
        stock = self.session.query(Stock).all()
        return stock
    
    def get_specify_stock(self, sector_name: str = None,
                          part_number: str = None,
                          status: str = None,
                          batch: str = None,
                          machining_batch: str = None,
                            assembly_batch: str = None
                          ):
        query = self.session.query(Stock)
        if sector_name is not None:
            query = query.filter(Stock.sector_name == sector_name)
        
        if part_number is not None:
            query = query.filter(Stock.part_number == part_number)

        if status is not None:
            query = query.filter(Stock.status == status)
        
        if batch is not None:
            query = query.filter(Stock.batch == batch)
        
        if machining_batch is not None:
            query = query.filter(Stock.machining_batch == machining_batch)

        if assembly_batch is not None:
            query = query.filter(Stock.assembly_batch == assembly_batch)
        
        query = query.order_by(Stock.entry_date.asc())

        return query.all()
    
    def get_stock_by_id(self, stock_id: int):
        stock = self.session.query(Stock).filter(Stock.ID==stock_id).first()
        return stock
    

    def update_Stock(self, stock:Stock):
        self.session.commit()
        self.session.refresh(stock)
        return stock
    
    def delete_stock(self, stock:Stock):
        self.session.delete(stock)
        self.session.commit()
        return True

    def transaction_rollback(self):
        self.session.rollback()