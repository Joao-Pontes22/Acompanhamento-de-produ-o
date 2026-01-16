
from app.domain.Value_objects.Sector import value_Sector
from datetime import datetime
from app.domain.Value_objects.Part_number import value_Part_number

#Exceptions
from app.domain.Exceptions import NotFoundException, StockInssuficientException

#Scheme
from app.Schemes.Stock_Schemes import Stock_Scheme,Stock_Transfer_Scheme,Stock_Scheme_models, Update_Stock_Scheme
# Repositórios
from app.repositories.Relation_repositorie import Relation_repositorie
from app.repositories.Stock_repositorie import Stock_repositorie
from app.repositories.Movimentation_repositorie import MovimentationRepository
from app.repositories.Sectors_repositorie import  Sectors_repositorie
from app.repositories.PartAndComp_repositorie import PartsAndComp_Repositorie
from app.repositories.Employers_repositories import employersRepo
# Entitys
from app.domain.Entitys.Transfer_entitys import Transfer_entitys
from app.domain.Entitys.Movimentation_entity import Movimentation_entity
from app.domain.Entitys.Stock_entitys import Stock_Entity, Stock_Entity_Part, Stock_Entity_Machined, Stock_Entity_Raw
class Stock_Services:
    def __init__(self, repo:Stock_repositorie, sectors_repo: Sectors_repositorie = None,
                 movimentation_repo: MovimentationRepository = None, 
                 partsAndComp_repo: PartsAndComp_Repositorie = None,
                 relation_repo: Relation_repositorie = None,
                 employers_repo: employersRepo = None ):
        self.repo = repo
        self.sectors_repo = sectors_repo
        self.partsAndComp_repo = partsAndComp_repo
        self.relation_repo = relation_repo
        self.movimentation_repo = movimentation_repo
        self.employers_repo = employers_repo

    def Service_Create_Stock(self, scheme:Stock_Scheme,
                            employer_id:int 
                            ):
        value_partnumber = value_Part_number(part_number=scheme.part_number)
        value_sector = value_Sector(sector=scheme.sector)
        employer = self.employers_repo.repo_find_by_id(id=employer_id)
        try:
            PartOrComp = self.partsAndComp_repo.repo_get_Parts_and_Components_by_part_number(part_number=value_partnumber.part_number)
            if not PartOrComp:
                raise NotFoundException("Item")
            sector = self.sectors_repo.repo_get_sector_by_name(name=value_sector.sector)
            if not sector:
                raise NotFoundException("Sector")
            batch = self.create_batch(item=PartOrComp)
            cost = scheme.qnty * PartOrComp.cost
            entity = Stock_Entity(scheme=scheme, cost=cost)
            if PartOrComp.category == "PART":
                self.create_stock_part(scheme=entity, PartOrComp=PartOrComp, batch=batch, employer=employer)

            elif PartOrComp.category == "COMPONENT":
                if PartOrComp.component_type == "MACHINED":
                    self.create_stock_machined(scheme=entity, PartOrComp=PartOrComp, batch=batch, employer=employer)
                elif PartOrComp.component_type == "RAW":
                    self.create_stock_raw(scheme=entity, PartOrComp= PartOrComp, batch=batch, employer=employer)
        except Exception as e:
            self.repo.session.rollback()
            raise e
            
    
    def service_get_all_stock(self):
        stock = self.repo.get_all_stock()
        if not stock:
            raise NotFoundException("Stock")
        return stock
    
    def service_get_filtered_stock(self, part_number: str = None,
                                         status:str = None,
                                         sector_name: str = None):
        value_sector = value_Sector(sector=sector_name) if sector_name else None
        stock = self.repo.get_specify_stock(sector_name=value_sector.sector if value_sector else None, status=status, part_number=part_number)
        if not stock:
            raise NotFoundException("Stock")
        return stock

    def Service_update_stock(self, stock_id:int,
                             scheme: Update_Stock_Scheme):
        stock = self.repo.get_stock_by_id(stock_id=stock_id)
        if not stock:
            raise NotFoundException("Stock")
        if scheme.qnty is not None:
            stock.qnty = scheme.qnty
        if scheme.reason is not None:
            stock.reason = scheme.reason
        updated_stock = self.repo.update_Stock(stock=stock)
        return updated_stock

    def Service_delete_stock(self, stock_id:int):
        stock = self.repo.get_stock_by_id(stock_id=stock_id)
        if not stock:
            raise NotFoundException("Stock")
        delete = self.repo.delete_stock(stock=stock)
        return delete

    def Service_Transfer_Stock(
        self,
        scheme: Stock_Transfer_Scheme,
        employer_id: int
        ):
        value_origin_sector = value_Sector(sector=scheme.origin_sector)
        value_destination_sector = value_Sector(sector=scheme.destination_sector)
        employer = self.employers_repo.repo_find_by_id( id=employer_id)
        origin = self.sectors_repo.repo_get_sector_by_name(name=value_origin_sector.sector)
        destination = self.sectors_repo.repo_get_sector_by_name(name=value_destination_sector.sector)

        if not origin:
            raise NotFoundException("Origin sector")
        if not destination:
            raise NotFoundException("Destination sector")

        transfer_entity = Transfer_entitys(part_number=scheme.part_number,
                                          origin_sector=scheme.origin_sector,
                                          destination_sector=scheme.destination_sector,
                                          qnty=scheme.qnty,
                                          batch=scheme.batch,
                                          machining_batch=scheme.machining_batch,
                                          assembly_batch=scheme.assembly_batch,
                                          reason=scheme.reason)
        stocks = self.repo.get_specify_stock(
            part_number=scheme.part_number,
            sector_name=value_origin_sector.sector
        )
        if not stocks:
            raise NotFoundException("Stock in origin sector")
        
        if sum([s.qnty for s in stocks]) < scheme.qnty:
            raise NotFoundException("Insufficient stock quantity in origin sector")
        self.transfer_stock(
                    stocks=stocks,
                    scheme=transfer_entity,
                    employer=employer.emp_id)
     

        return {"message": "Stock transferred successfully"}
    
    def consume_stock(self, relation,
                            scheme:Stock_Entity,
                            employer:str):
        for items in relation:
            component = self.partsAndComp_repo.repo_get_Parts_and_Components_by_part_number(part_number=items.consume_item_Part_number)
            stock = self.repo.get_specify_stock(part_number=component.part_number, sector_name=scheme.sector_name)
            total_qnty = sum([s.qnty for s in stock])
            if total_qnty < scheme.qnty:
                raise StockInssuficientException(part_number=component.part_number, required=scheme.qnty, available=total_qnty)
            remaining_qnty = scheme.qnty
            for s in stock:
                if remaining_qnty <= 0:
                    break
                consume = min(s.qnty, remaining_qnty)
                s.qnty -= consume
                remaining_qnty -= consume
                self.repo.update_Stock(stock=s)
                movi_entity_consumption = Movimentation_entity(part_number=component.part_number,
                                                            origin=scheme.sector,
                                                            reason=f"Consumption for part {scheme.part_number}, batch {s.batch}",
                                                            movimentation_type="CONSUME",
                                                            employer=employer,
                                                            batch=scheme.batch if scheme.batch else None,
                                                            qnty=consume,
                                                            date=datetime.today(),
                                                            destination=scheme.sector,
                                                            machining_batch=scheme.machining_batch if scheme.machining_batch else None,
                                                            assembly_batch=scheme.assembly_batch if scheme.assembly_batch else None)
                self.movimentation_repo.create(movimentation_data=movi_entity_consumption)
                self.repo.delete_stock(stock=s) if s.qnty == 0 else None

    def transfer_stock(self, stocks,
                            scheme:Stock_Transfer_Scheme,
                            employer:str):
        remaining_qnty = scheme.qnty
        for stock in stocks:
            
            if remaining_qnty <= 0:
                break
            transfer_qnty = min(stock.qnty, remaining_qnty)
            stock.qnty -= transfer_qnty
            remaining_qnty -= transfer_qnty
            self.repo.update_Stock(stock=stock)
            movi_entity_consumption = Movimentation_entity(part_number=stock.part_number,
                                                        origin=scheme.origin_sector,
                                                        reason=scheme.reason,
                                                        movimentation_type="TRANSFER_OUT",
                                                        employer=employer,
                                                        batch=stock.batch,
                                                        qnty=transfer_qnty,
                                                        date=datetime.today(),
                                                        destination=scheme.destination_sector,
                                                        machining_batch=stock.machining_batch,
                                                        assembly_batch=stock.assembly_batch)
            self.repo.create_stock(scheme=Stock_Scheme_models(
                sector_name=scheme.destination_sector,
                part_number=stock.part_number,
                batch=stock.batch,
                machining_batch=stock.machining_batch,
                machining_date=stock.machining_date,
                assembly_batch=stock.assembly_batch,
                assembly_date=stock.assembly_date,
                qnty=transfer_qnty,
                entry_date=stock.entry_date,
                supplier_name=stock.supplier,
                client_name=stock.client,
                status=stock.status,
                cost=stock.cost
            ))
            if stock.qnty == 0:
                self.repo.delete_stock(stock=stock)
            self.movimentation_repo.create(movimentation_data=movi_entity_consumption)
            
            movi_entity_transfer = Movimentation_entity(part_number=stock.part_number,
                                                origin=scheme.origin_sector,
                                                reason=scheme.reason,
                                                movimentation_type="TRANSFER_IN",
                                                employer=employer,
                                                batch=stock.batch,
                                                qnty=transfer_qnty,
                                                date=datetime.today(),
                                                destination=scheme.destination_sector,
                                                machining_batch=stock.machining_batch,
                                                assembly_batch=stock.assembly_batch)
            self.movimentation_repo.create(movimentation_data=movi_entity_transfer)
    
    def create_batch(self, item):
        if item.category == "PART":
            last_batch = self.movimentation_repo.get_movimentation_filtered_first(part_number=item.part_number, date=True)
            if last_batch:
                return int(last_batch.assembly_batch) + 1
            else:
                return int(1) 
        elif item.category == "COMPONENT" and item.component_type == "MACHINED":
            last_batch = self.movimentation_repo.get_movimentation_filtered_first(part_number=item.part_number, date=True)
            if last_batch:
                return int(last_batch.machining_batch) + 1
            else:
                return int(1)   
        elif item.category == "COMPONENT" and item.component_type == "RAW":
            last_batch = self.movimentation_repo.get_movimentation_filtered_first(part_number=item.part_number, date=True)
            if last_batch:
                return int(last_batch.batch) + 1
            else:
                return int(1) 
        

    def create_stock_part(self, scheme: Stock_Entity, PartOrComp, batch, employer):
       
            entity = Stock_Entity_Part(scheme=scheme, 
                                       client=PartOrComp.client_name,
                                       assembly_batch=batch,
                                       assembly_date=datetime.today(),
                                       )
            relation = self.relation_repo.get_relations_filtred(create_item_part_number=PartOrComp.part_number)
            if not relation:
                raise NotFoundException("Relation")
            consume = self.consume_stock(relation=relation,
                                                        scheme=entity,
                                                        employer=employer,
                                                        sector_name=scheme.sector)
                
                
            movi_entity = Movimentation_entity(part_number=scheme.part_number,
                                                origin=scheme.sector,
                                                reason=scheme.reason,
                                                movimentation_type="CREATE",
                                                employer=employer,
                                                batch=None,
                                                qnty=entity.qnty,
                                                date=datetime.today(),
                                                destination=entity.sector,
                                                machining_batch=None,
                                                assembly_batch=str(batch))
            new_stock = self.repo.create_stock(scheme=entity)
            movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity)
            return new_stock
    
    def create_stock_machined(self, scheme: Stock_Entity, PartOrComp, batch, employer):
       
            entity = Stock_Entity_Machined(scheme=scheme, supplier= PartOrComp.supplier_name,
                                       assembly_batch=batch,
                                       assembly_date=datetime.today(),
                                       )
            relation = self.relation_repo.get_relations_filtred(create_item_part_number=PartOrComp.part_number)
            if not relation:
                raise NotFoundException("Relation")
            consume = self.consume_stock(relation=relation,
                                                        scheme=entity,
                                                        employer=employer,
                                                        sector_name=scheme.sector)
                
                
            movi_entity = Movimentation_entity(part_number=scheme.part_number,
                                                origin=scheme.sector,
                                                reason=scheme.reason,
                                                movimentation_type="CREATE",
                                                employer=employer,
                                                batch=None,
                                                qnty=entity.qnty,
                                                date=datetime.today(),
                                                destination=entity.sector,
                                                machining_batch=None,
                                                assembly_batch=str(batch))
            new_stock = self.repo.create_stock(scheme=entity)
            movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity)
            return new_stock
    
    def create_stock_raw(self, scheme: Stock_Entity, PartOrComp, batch, employer):
        entity = Stock_Entity_Raw(scheme=scheme, 
                                    batch=str(batch),
                                    entry_date=datetime.today(),
                                    supplier=PartOrComp.supplier_name)
        
        movi_entity = Movimentation_entity(part_number=entity.part_number,
                                                origin=entity.sector,
                                                reason=entity.reason,
                                                movimentation_type="CREATE",
                                                employer=employer,
                                                batch=entity.batch,
                                                qnty=entity.qnty,
                                                date=datetime.today(),
                                                destination=entity.sector,
                                                machining_batch=entity.machining_batch,
                                                assembly_batch=entity.assembly_batch)
        new_stock = self.repo.create_stock(scheme=entity)
        movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity,)
        return new_stock