from app.models.Stock import Stock


class StockRepository:
    def __init__(self, session):
        self.session = session
        pass 

    

    def create_stock(self,sector_name: str,
                     part_number: str,
                     batch: str,
                     machining_batch: str,
                     machining_date,
                     assembly_batch: str,
                     assembly_date,
                     qnty:int,
                     entry_date,
                     supplier_name: str,
                     status: str,
                     cost: float,
                     client_name: str
                     ):
        new_stock = Stock(sector_name=sector_name,
                          part_number=part_number,
                          batch=batch,
                          machining_batch=machining_batch,
                          machining_date=machining_date,
                          assembly_batch=assembly_batch,
                          assembly_date=assembly_date,
                          qnty=qnty,
                          entry_date=entry_date, 
                          supplier_name=supplier_name, 
                          status=status, 
                          cost=cost,
                          client_name=client_name
                          )
        self.session.add(new_stock)
        self.session.commit()
        return new_stock
    
   
    def get_all_stock(self) -> list[Stock]:
        stock = self.session.query(Stock).all()
        return stock
    
    def get_filtred_stock(self, sector_name: str = None,
                          part_number: str = None,
                          status: str = None,
                          batch: str = None,
                          machining_batch: str = None,
                          assembly_batch: str = None 
                         ) -> list[Stock]:
        
        query = self.session.query(Stock)
        if sector_name:
            query = query.filter(Stock.sector_name == sector_name)
        
        if part_number:
            query = query.filter(Stock.part_number == part_number)

        if status:
            query = query.filter(Stock.status == status)
        
        if batch:
            query = query.filter(Stock.batch == batch)
        
        if machining_batch:
            query = query.filter(Stock.machining_batch == machining_batch)

        if assembly_batch:
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