from app.Schemes.Stock_Schemes import Stock_Scheme_Part,Stock_Transfer_Scheme, Stock_Scheme_Raw_Coponent,Stock_Scheme_models, Stock_Scheme_machined_Coponent, Update_Raw_Stock_Scheme, Update_Part_Stock_Scheme, Update_Machined_Stock_Scheme
from app.domain.Entitys.Stock_entitys import Stock_Entity_Parts, Stock_Entity_Raw_Component, Stock_Entity_machined_Component, Updated_Part_Stock_Entity, Update_Machined_Stock_Scheme, Update_Raw_Stock_Scheme
from app.domain.Exceptions import NotFoundException
from app.repositories.RelationPartsxComponents_repositorie import RelationPartsxComponents_repositorie
from app.repositories.Movimentation_repositorie import MovimentationRepository
from app.repositories.Sectors_repositorie import  Sectors_repositorie
from app.repositories.Components_repositorie import Components_Repositorie
from app.repositories.Parts_repositorie import Parts_Repositorie
from app.repositories.Stock_repositorie import Stock_repositorie
from app.domain.Entitys.Movimentation_entity import Movimentation_entity
from app.repositories.RelationMachinedxRaw_repositorie import RelationMachinedxRaw_repositorie
from app.domain.Entitys.Transfer_entitys import Transfer_entitys
from datetime import datetime

class Stock_Services:
    def __init__(self, repo:Stock_repositorie, sectors_repo: Sectors_repositorie = None,
                 movimentation_repo: MovimentationRepository = None, 
                 parts_repo: Parts_Repositorie = None,
                 relation_Partsxcomp_repo: RelationPartsxComponents_repositorie = None,
                 relation_MachinedxRaw_repo: RelationMachinedxRaw_repositorie = None,
                 components_repo: Components_Repositorie= None):
        self.repo = repo
        self.sectors_repo = sectors_repo
        self.parts_repo = parts_repo
        self.relation_Partsxcomp_repo = relation_Partsxcomp_repo
        self.movimentation_repo = movimentation_repo
        self.components_repo = components_repo
        self.relation_MachinedxRaw_repo = relation_MachinedxRaw_repo

    def Service_Create_Part_Stock(self, scheme:Stock_Scheme_Part,
                            employer_id:int 
                            ):
        part = self.parts_repo.repo_get_Parts_by_part_number(part_number=scheme.part_number)
        sector = self.sectors_repo.repo_get_sector_by_id(id=scheme.sector_ID)
        if not part:
            raise NotFoundException("Part")
        if not sector:
            raise NotFoundException("Sector")
        relation = self.relation_Partsxcomp_repo.get_relations_by_part_id(part_ID=part.id)
        if not relation:
            raise NotFoundException("Relation")
        with self.repo.transaction_begin():
            consume = self.consume_machined_stock(relation=relation,
                                                    scheme=scheme,
                                                    employer_id=employer_id)
            cost = scheme.qnty * part.cost
            entity = Stock_Entity_Parts(scheme=scheme, cost=cost, client_id=part.client_ID)
            movi_entity = Movimentation_entity(part_number=scheme.part_number,
                                            origin=scheme.sector_ID,
                                            reason=scheme.reason,
                                            movimentation_type="CREATE",
                                            employer_id=employer_id,
                                            batch=None,
                                            qnty=scheme.qnty,
                                            date=datetime.today(),
                                            destination=scheme.sector_ID,
                                            machining_batch=None,
                                            assembly_batch=scheme.assembly_batch)
            new_stock = self.repo.create_Part_stock(scheme=entity)
            movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity)
        return new_stock
    
    def Service_Create_Machined_Component_Stock(self, scheme:Stock_Scheme_machined_Coponent,
                                employer_id: int
                                ):
        component = self.components_repo.repo_get_machined_components(part_number=scheme.part_number)
        sector = self.sectors_repo.repo_get_sector_by_id(id=scheme.sector_ID)
        if not component:
            raise NotFoundException("Machined Component")
        if not sector:
            raise NotFoundException("Sector")
        relation = self.relation_MachinedxRaw_repo.get_relation_by_machined_id(machined_ID=component.id)
        if not relation:
            raise NotFoundException("Relation")
        raw_component = self.components_repo.repo_get_Component_by_id(id=relation.raw_ID)
        if not raw_component:
            raise NotFoundException("Raw Component")
        stock_list = self.repo.get_specify_stock(part_number=raw_component.part_number, sector_id=scheme.sector_ID)
        with self.repo.transaction_begin():
            self.consume_raw_stock(raw_component=raw_component,
                                scheme=scheme,
                                employer_id=employer_id,
                                stock_list=stock_list)
            cost = scheme.qnty * component.cost
            entity = Stock_Entity_machined_Component(scheme=scheme, cost=cost, supplier_id=component.supplier_ID)
            movi_entity = Movimentation_entity(part_number=scheme.part_number,
                                            origin=scheme.sector_ID,
                                            reason=scheme.reason,
                                            movimentation_type="CREATE",
                                            employer_id=employer_id,
                                            batch=None,
                                            qnty=scheme.qnty,
                                            date=datetime.today(),
                                            destination=scheme.sector_ID,
                                            machining_batch=scheme.machining_batch,
                                            assembly_batch=None)
            new_stock = self.repo.create_Machined_Component_stock(scheme=entity)
            movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity)
        return new_stock
    
    def Service_Create_Raw_Component_Stock(self, scheme:Stock_Scheme_Raw_Coponent,
                            employer_id: int 
                            ):
        component = self.components_repo.repo_get_raw_components(part_number=scheme.part_number)
        sector = self.sectors_repo.repo_get_sector_by_id(id=scheme.sector_ID)
        if not component:
            raise NotFoundException("Raw Component")
        if not sector:
            raise NotFoundException("Sector")
        cost = scheme.qnty * component.cost
        entity = Stock_Entity_Raw_Component(scheme=scheme, cost=cost, supplier_id=component.supplier_ID)
        movi_entity = Movimentation_entity(part_number=scheme.part_number,
                                           origin=scheme.sector_ID,
                                           reason=scheme.reason,
                                           movimentation_type="CREATE",
                                           employer_id=employer_id,
                                           batch=scheme.batch,
                                           qnty=scheme.qnty,
                                           date=datetime.today(),
                                           destination=scheme.sector_ID,
                                           machining_batch=None,
                                           assembly_batch=None)
        new_stock = self.repo.create_Raw_Component_stock(scheme=entity)
        movi_repo = self.movimentation_repo.create(movimentation_data=movi_entity)
        return new_stock
    

    def service_get_all_stock(self):
        stock = self.repo.get_all_stock()
        if not stock:
            raise NotFoundException("Stock")
        return stock
    
    def service_get_filtered_stock(self, part_number: str = None,
                                         status:str = None,
                                         sector_id: int = None):
        stock = self.repo.get_specify_stock(sector_id=sector_id, status=status, part_number=part_number)
        if not stock:
            raise NotFoundException("Stock")
        return stock


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
        if scheme.qnty <= 0:
            raise ValueError("Quantity must be greater than zero")

        origin = self.sectors_repo.repo_get_sector_by_id(scheme.origin_sector_id)
        destination = self.sectors_repo.repo_get_sector_by_id(scheme.destination_sector_id)

        if not origin:
            raise NotFoundException("Origin sector")
        if not destination:
            raise NotFoundException("Destination sector")

        transfer_entity = Transfer_entitys(part_number=scheme.part_number,
                                          origin_sector_id=scheme.origin_sector_id,
                                          destination_sector_id=scheme.destination_sector_id,
                                          qnty=scheme.qnty,
                                          batch=scheme.batch,
                                          machining_batch=scheme.machining_batch,
                                          assembly_batch=scheme.assembly_batch,
                                          reason=scheme.reason)
        stocks = self.repo.get_specify_stock(
            part_number=scheme.part_number,
            sector_id=scheme.origin_sector_id
        )
        if not stocks:
            raise NotFoundException("Stock in origin sector")
        
        if sum([s.qnty for s in stocks]) < scheme.qnty:
            raise NotFoundException("Insufficient stock quantity in origin sector")
        self.transfer_stock(
                    stocks=stocks,
                    scheme=transfer_entity,
                    employer_id=employer_id)
     

        return {"message": "Stock transferred successfully"}
    
    def consume_machined_stock(self, relation,
                            scheme:Stock_Scheme_Part,
                            employer_id:int):
        for components in relation:
            component = self.components_repo.repo_get_Component_by_id(id=components.components_ID)
            stock = self.repo.get_specify_stock(part_number=component.part_number, sector_id=scheme.sector_ID)
            total_qnty = sum([s.qnty for s in stock])
            if total_qnty < scheme.qnty:
                raise NotFoundException(f"Insufficient stock for component {component.part_number}")
            remaining_qnty = scheme.qnty
            for s in stock:
                if remaining_qnty <= 0:
                    break
                consume = min(s.qnty, remaining_qnty)
                s.qnty -= consume
                remaining_qnty -= consume
                self.repo.update_Stock(stock=s)
                movi_entity_consumption = Movimentation_entity(part_number=component.part_number,
                                                            origin=scheme.sector_ID,
                                                            reason=f"Consumption for part {scheme.part_number}, batch {s.batch}",
                                                            movimentation_type="CONSUME",
                                                            employer_id=employer_id,
                                                            batch=s.batch,
                                                            qnty=consume,
                                                            date=datetime.today(),
                                                            destination=None,
                                                            machining_batch=None,
                                                            assembly_batch=scheme.assembly_batch)
                self.movimentation_repo.create(movimentation_data=movi_entity_consumption)
                self.repo.delete_stock(stock=s) if s.qnty == 0 else None


    def consume_raw_stock(self, raw_component,
                          scheme:Stock_Scheme_machined_Coponent,
                          employer_id:int,
                          stock_list):
        total_qnty = sum([stock.qnty for stock in stock_list])
        if total_qnty < scheme.qnty:
            raise NotFoundException("Insufficient raw component stock")
        remaining_qnty = scheme.qnty
        for stock in stock_list:
            if remaining_qnty <= 0:
                break
            consume = min(stock.qnty, remaining_qnty)
            stock.qnty -= consume
            remaining_qnty -= consume
            self.repo.update_Stock(stock=stock)
            movi_entity_consumption = Movimentation_entity(part_number=raw_component.part_number,
                                                        origin=scheme.sector_ID,
                                                        reason=f"Consumption for machining {scheme.part_number}, batch {scheme.machining_batch}",
                                                        movimentation_type="CONSUME",
                                                        employer_id=employer_id,
                                                        batch=stock.batch,
                                                        qnty=consume,
                                                        date=datetime.today(),
                                                        destination=None,
                                                        machining_batch=scheme.machining_batch,
                                                        assembly_batch=None)
            self.movimentation_repo.create(movimentation_data=movi_entity_consumption)
            self.repo.delete_stock(stock=stock) if stock.qnty == 0 else None

    

    def transfer_stock(self, stocks,
                            scheme:Stock_Transfer_Scheme,
                            employer_id:int):
        remaining_qnty = scheme.qnty
        for stock in stocks:
            
            if remaining_qnty <= 0:
                break
            transfer_qnty = min(stock.qnty, remaining_qnty)
            stock.qnty -= transfer_qnty
            remaining_qnty -= transfer_qnty
            self.repo.update_Stock(stock=stock)
            movi_entity_consumption = Movimentation_entity(part_number=stock.part_number,
                                                        origin=scheme.origin_sector_id,
                                                        reason=scheme.reason,
                                                        movimentation_type="TRANSFER_OUT",
                                                        employer_id=employer_id,
                                                        batch=stock.batch,
                                                        qnty=transfer_qnty,
                                                        date=datetime.today(),
                                                        destination=scheme.destination_sector_id,
                                                        machining_batch=stock.machining_batch,
                                                        assembly_batch=stock.assembly_batch)
            self.repo.create_stock(scheme=Stock_Scheme_models(
                sector_ID=scheme.destination_sector_id,
                part_number=stock.part_number,
                batch=stock.batch,
                machining_batch=stock.machining_batch,
                machining_date=stock.machining_date,
                assembly_batch=stock.assembly_batch,
                assembly_date=stock.assembly_date,
                qnty=transfer_qnty,
                entry_date=stock.entry_date,
                supplier_ID=stock.supplier_ID,
                client_ID=stock.client_ID,
                status=stock.status,
                cost=stock.cost
            ))
            if stock.qnty == 0:
                self.repo.delete_stock(stock=stock)
            self.movimentation_repo.create(movimentation_data=movi_entity_consumption)
            
            movi_entity_transfer = Movimentation_entity(part_number=stock.part_number,
                                                origin=scheme.origin_sector_id,
                                                reason=scheme.reason,
                                                movimentation_type="TRANSFER_IN",
                                                employer_id=employer_id,
                                                batch=stock.batch,
                                                qnty=transfer_qnty,
                                                date=datetime.today(),
                                                destination=scheme.destination_sector_id,
                                                machining_batch=stock.machining_batch,
                                                assembly_batch=stock.assembly_batch)
            self.movimentation_repo.create(movimentation_data=movi_entity_transfer)


    def create_stock(self, scheme:Stock_Scheme_models):

        new_stock = self.repo.create_stock(scheme=scheme)
        
        return new_stock
    

