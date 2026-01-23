#Date time
from datetime import datetime
#Exceptions
from app.domain.Exceptions import NotFoundException, StockInssuficientException
#Scheme
from app.Schemas.Stock_Schemas import StockSchema,StockTransferSchema, UpdateStockInfoSchema
from app.Schemas.Queries.stock_query_params import StockParameters
# Repositórios
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Stock_repository import StockRepository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.repositories.Sectors_repository import  SectorsRepository
from app.repositories.PartAndComp_repository import PartsAndCompRepository
from app.repositories.Employers_repository import EmployersRepository
# Entitys
from app.domain.Entitys.Transfer_entitys import TransferEntity
from app.domain.Entitys.Movimentation_entity import MovimentationEntity
from app.domain.Entitys.Stock_entitys import StockEntity, StockEntityRaw, StockEntity, StockEntityMachined, StockEntityPart
#Value Objects
from app.domain.Value_objects.Part_number import value_Part_number
from app.domain.Value_objects.Sector import valueSector
from app.domain.Value_objects.Status import valueStatus
from app.domain.Value_objects.Batchs import ValueBatchs

class StockService:
    def __init__(self, repo:StockRepository, sectors_repo: SectorsRepository = None,
                 movimentation_repo: MovimentationRepository = None, 
                 partsAndComp_repo: PartsAndCompRepository = None,
                 relation_repo: RelationRepository = None,
                 employers_repo: EmployersRepository = None 
                 ):
        
        self.repo = repo
        self.sectors_repo = sectors_repo
        self.partsAndComp_repo = partsAndComp_repo
        self.relation_repo = relation_repo
        self.movimentation_repo = movimentation_repo
        self.employers_repo = employers_repo

    def create_stock(self, schema:StockSchema,
                            employer_id:int 
                            ):

        employer = self.employers_repo.get_by_id(id=employer_id)
        try:

            PartOrComp = self.partsAndComp_repo.get_Parts_and_Components_by_part_number(part_number=schema.part_number)
            if not PartOrComp:
                raise NotFoundException("Part Number")
            
            sector = self.sectors_repo.get_sector_by_name(name=schema.sector_name)
            if not sector:
                raise NotFoundException("Sector")
            
            batch = self.create_batch(item=PartOrComp)
            cost = schema.qnty * PartOrComp.cost

            entity = StockEntity(sector_name=schema.sector_name,
                                 part_number=schema.part_number,
                                 qnty=schema.qnty,
                                 reason=schema.reason, 
                                 cost=cost
                                 )
            
            if PartOrComp.category == "PART":
                new_stock = self.create_stock_part(scheme=entity, 
                                                   PartOrComp=PartOrComp, 
                                                   batch=batch, 
                                                   emp_id=employer.emp_id
                                                   )
                return new_stock
            
            elif PartOrComp.category == "COMPONENT":
                if PartOrComp.component_type == "MACHINED":
                    new_stock = self.create_stock_machined(scheme=entity, 
                                                           PartOrComp=PartOrComp, 
                                                           batch=batch, 
                                                           emp_id=employer.emp_id
                                                           )
                    return new_stock
                
                elif PartOrComp.component_type == "RAW":
                    new_stock = self.create_stock_raw(scheme=entity, 
                                                      PartOrComp= PartOrComp, 
                                                      batch=batch, 
                                                      emp_id=employer.emp_id
                                                      )
                    return new_stock
                
        except Exception as e:
            self.repo.session.rollback()
            
    
    def get_all_stock(self) -> list:

        stock = self.repo.get_all_stock()
        if not stock:
            raise NotFoundException("Stock")
        
        return stock
    
    def get_filtred_stock(self, 
                           query_params: StockParameters,
                            ) -> list:
        stock = self.repo.get_filtred_stock(sector_name=query_params.sector_name, 
                                            status=query_params.status, 
                                            part_number=query_params.part_number,
                                            batch=query_params.batch,
                                            assembly_batch=query_params.assembly_batch,
                                            machining_batch=query_params.machining_batch
                                            )
        if not stock:
            raise NotFoundException("Stock")
        
        return stock

    def update_stock(self, 
                     stock_id:int,
                     schema: UpdateStockInfoSchema):
        
        stock = self.repo.get_stock_by_id(stock_id=stock_id)
        if not stock:
            raise NotFoundException("Stock")
        for field, value in schema.model_dump(exclude_unset=True):
            setattr(stock, field, value)

        updated_stock = self.repo.update_Stock(stock=stock)
        return updated_stock

    def delete_stock(self, stock_id:int):

        stock = self.repo.get_stock_by_id(stock_id=stock_id)
        if not stock:
            raise NotFoundException("Stock")
        
        delete = self.repo.delete_stock(stock=stock)

        return delete

    def transfer_sector_stock(self,
                              schema: StockTransferSchema,
                              employer_id: int,
                              part_number : str,
                              origin_sector: str,
                              batch: str = None,
                              machining_batch: str = None,
                              assembly_batch: str = None,
                              ):
        try:
            value_sector = valueSector(sector_name=origin_sector)
            value_part_number = value_Part_number(part_number=part_number)
            value_batch = ValueBatchs(batch=batch)
            value_assembly_batch = ValueBatchs(batch=assembly_batch)
            value_machining_batch = ValueBatchs(batch=machining_batch)
            employer = self.employers_repo.get_by_id( id=employer_id)
            sector_origin = self.sectors_repo.get_sector_by_name(name=value_sector.sector_name)
            sector_destination = self.sectors_repo.get_sector_by_name(name=schema.destination_sector)

            if not sector_origin:
                raise NotFoundException("Origin sector")
            if not sector_destination:
                raise NotFoundException("Destination sector")

            entity = TransferEntity(part_number=value_part_number.part_number,
                                            origin_sector=value_sector.sector_name,
                                            destination_sector=schema.destination_sector,
                                            qnty=schema.qnty,
                                            batch=value_batch.batch,
                                            machining_batch=value_machining_batch.batch,
                                            assembly_batch=value_assembly_batch.batch,
                                            reason=schema.reason)
            
            stocks = self.repo.get_filtred_stock(part_number=entity.part_number,
                                                 sector_name=entity.origin_sector
                                                )
            if not stocks:
                raise NotFoundException("Stock in origin sector")
            
            if sum([s.qnty for s in stocks]) < schema.qnty:
                raise StockInssuficientException("Insufficient stock quantity in origin sector")
            
            self.transfer_stock(stocks=stocks,
                                schema=entity,
                                employer=employer)
        
            return {"message": "Stock transferred successfully"}
        except Exception as e:
            self.repo.session.rollback()
    
    def consume_stock(self, relation,
                            schema:StockEntity,
                            emp_id:str):
        try:
            for items in relation:

                component = self.partsAndComp_repo.get_Parts_and_Components_by_part_number(part_number=items.consume_item_part_number)
                stock = self.repo.get_filtred_stock(part_number=component.part_number, 
                                                    sector_name=schema.sector_name
                                                    )
                
                total_qnty = sum([s.qnty for s in stock])

                if total_qnty < schema.qnty:
                    raise StockInssuficientException(part_number=component.part_number, required=schema.qnty, available=total_qnty)
                
                remaining_qnty = schema.qnty
                for s in stock:
                    if remaining_qnty <= 0:
                        break

                    consume = min(s.qnty, remaining_qnty)

                    s.qnty -= consume
                    remaining_qnty -= consume

                    self.repo.update_Stock(stock=s)

                    movi_entity_consumption = MovimentationEntity(part_number=component.part_number,
                                                                sector_origin=schema.sector_name,
                                                                reason=f"Consumption for part {schema.part_number}, batch {s.batch}",
                                                                movimentation_type="CONSUME",
                                                                emp_id=emp_id,
                                                                batch=s.batch,
                                                                qnty=consume,
                                                                date=datetime.today(),
                                                                sector_destination=schema.sector_name,
                                                                machining_batch=s.machining_batch,
                                                                assembly_batch=s.assembly_batch)
                    self.movimentation_repo.create(movimentation_data=movi_entity_consumption)

                    self.repo.delete_stock(stock=s) if s.qnty == 0 else None

        except Exception as e:
            self.repo.session.rollback()

    def transfer_stock(self, stocks,
                            schema:StockTransferSchema,
                            emp_id:str):
        try:
            remaining_qnty = schema.qnty

            for stock in stocks:
                if remaining_qnty <= 0:
                    break
                transfer_qnty = min(stock.qnty, remaining_qnty)
                stock.qnty -= transfer_qnty
                remaining_qnty -= transfer_qnty
                self.repo.update_Stock(stock=stock)

                movi_entity_consumption = MovimentationEntity(part_number=stock.part_number,
                                                            sector_origin=schema.origin_sector,
                                                            reason=schema.reason,
                                                            movimentation_type="TRANSFER_OUT",
                                                            emp_id=emp_id,
                                                            batch=stock.batch,
                                                            qnty=transfer_qnty,
                                                            date=datetime.today(),
                                                            sector_destination=schema.destination_sector,
                                                            machining_batch=stock.machining_batch,
                                                            assembly_batch=stock.assembly_batch)
                
                self.repo.create_stock(sector_name=stock.destination_sector,
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
                                        )
                if stock.qnty == 0:
                    self.repo.delete_stock(stock=stock)
                self.movimentation_repo.create_movimentation(movimentation_data=movi_entity_consumption)
                
                movi_entity_transfer = MovimentationEntity(part_number=stock.part_number,
                                                    origin=schema.origin_sector,
                                                    reason=schema.reason,
                                                    movimentation_type="TRANSFER_IN",
                                                    emp_id=emp_id,
                                                    batch=stock.batch,
                                                    qnty=transfer_qnty,
                                                    date=datetime.today(),
                                                    destination=schema.destination_sector,
                                                    machining_batch=stock.machining_batch,
                                                    assembly_batch=stock.assembly_batch
                                                    )
                
                self.movimentation_repo.create_movimentation(movimentation_data=movi_entity_transfer)
        except Exception as e:
            self.repo.session.rollback()
    
    def create_batch(self, item):
        
        if item.category == "PART":
            last_batch = self.movimentation_repo.get_movimentation_create_stock_filtered_first(part_number=item.part_number, movimentation_id=True)
            if last_batch:
                return int(last_batch.assembly_batch) + 1
            else:
                return int(1) 
        elif item.category == "COMPONENT" and item.component_type == "MACHINED":
            last_batch = self.movimentation_repo.get_movimentation_create_stock_filtered_first(part_number=item.part_number, movimentation_id=True)
            if last_batch:
                return int(last_batch.machining_batch) + 1
            else:
                return int(1)   
        elif item.category == "COMPONENT" and item.component_type == "RAW":
            last_batch = self.movimentation_repo.get_movimentation_create_stock_filtered_first(part_number=item.part_number, movimentation_id=True)
            if last_batch:
                return int(last_batch.batch) + 1
            else:
                return int(1) 
        
    def create_stock_part(self, 
                          schema: StockEntity, 
                          PartOrComp, batch, 
                          emp_id: str
                          ):
        try:
                entity = StockEntityPart(sector_name=schema.sector_name,
                                         part_number=schema.part_number,
                                         qnty=schema.qnty,
                                         reason=schema.reason,
                                         cost=schema.cost, 
                                         client=PartOrComp.client_name,
                                         assembly_batch=str(batch),
                                         assembly_date=datetime.today(),
                                         )
                relation = self.relation_repo.get_relations_filtred(create_item_part_number=PartOrComp.part_number)
                if not relation:
                    raise NotFoundException("Relation")
                movi_entity = MovimentationEntity(part_number=entity.part_number,
                                                    sector_origin=entity.sector_name,
                                                    reason=entity.reason,
                                                    movimentation_type="CREATE",
                                                    emp_id=emp_id,
                                                    batch=None,
                                                    qnty=entity.qnty,
                                                    date=datetime.today(),
                                                    sector_destination=entity.sector_name,
                                                    machining_batch=None,
                                                    assembly_batch=str(batch))
                
                movi_repo = self.movimentation_repo.create_movimentation(part_number=movi_entity.part_number,
                                                                     sector_origin=movi_entity.sector_origin,
                                                                     reason=movi_entity.reason,
                                                                     movimentation_type=movi_entity.movimentation_type,
                                                                     emp_id=movi_entity.emp_id,
                                                                     batch=movi_entity.batch,
                                                                     qnty=movi_entity.qnty,
                                                                     date=movi_entity.date,
                                                                     sector_destination=movi_entity.sector_destination,
                                                                     machining_batch=movi_entity.machining_batch,
                                                                     assembly_batch=movi_entity.assembly_batch
                                                                     )
                consume = self.consume_stock(relation=relation,
                                            scheme=entity,
                                            emp_id=entity.emp_id)     
                
                new_stock = self.repo.create_stock(scheme=entity)
                return new_stock
        except Exception as e:
           self.repo.session.rollback()
    
    def create_stock_machined(self, 
                              schema: StockEntity, 
                              PartOrComp, 
                              batch: str, 
                              emp_id: str):
       try:
            entity = StockEntityMachined(scheme=schema, 
                                         supplier= PartOrComp.supplier_name,
                                         machining_batch=batch,
                                         machining_date=datetime.today(),
                                        )
            relation = self.relation_repo.get_relations_filtred(create_item_part_number=PartOrComp.part_number)
            if not relation:
                raise NotFoundException("Relation")
            consume = self.consume_stock(relation=relation,
                                         scheme=entity,
                                         emp_id=emp_id)          
            movi_entity = MovimentationEntity(part_number=schema.part_number,
                                                sector_origin=schema.sector_name,
                                                reason=schema.reason,
                                                movimentation_type="CREATE",
                                                emp_id=emp_id,
                                                batch=None,
                                                qnty=entity.qnty,
                                                date=datetime.today(),
                                                sector_destination=entity.sector_name,
                                                machining_batch=str(batch),
                                                assembly_batch=None)
            
            movi_repo = self.movimentation_repo.create_movimentation(part_number=movi_entity.part_number,
                                                                     sector_origin=movi_entity.sector_origin,
                                                                     reason=movi_entity.reason,
                                                                     movimentation_type=movi_entity.movimentation_type,
                                                                     emp_id=movi_entity.emp_id,
                                                                     batch=movi_entity.batch,
                                                                     qnty=movi_entity.qnty,
                                                                     date=movi_entity.date,
                                                                     sector_destination=movi_entity.sector_destination,
                                                                     machining_batch=movi_entity.machining_batch,
                                                                     assembly_batch=movi_entity.assembly_batch
                                                                     )
            new_stock = self.repo.create_stock(scheme=entity)
            
            return new_stock
       except Exception as e:
           self.repo.session.rollback()
           raise Exception("Error 500")
    
    def create_stock_raw(self, schema: StockEntity, PartOrComp, batch, employer):
        try:
                entity = StockEntityRaw(scheme=schema, 
                                            batch=str(batch),
                                            entry_date=datetime.today(),
                                            supplier=PartOrComp.supplier_name)
                
                movi_entity = MovimentationEntity(part_number=entity.part_number,
                                                        sector_origin=entity.sector_name,
                                                        reason=entity.reason,
                                                        movimentation_type="CREATE",
                                                        employer=employer.emp_id,
                                                        batch=entity.batch,
                                                        qnty=entity.qnty,
                                                        date=datetime.today(),
                                                        sector_destination=entity.sector_name,
                                                        machining_batch=entity.machining_batch,
                                                        assembly_batch=entity.assembly_batch)
                
                movi_repo = self.movimentation_repo.create_movimentation(part_number=movi_entity.part_number,
                                                                     sector_origin=movi_entity.sector_origin,
                                                                     reason=movi_entity.reason,
                                                                     movimentation_type=movi_entity.movimentation_type,
                                                                     emp_id=movi_entity.emp_id,
                                                                     batch=movi_entity.batch,
                                                                     qnty=movi_entity.qnty,
                                                                     date=movi_entity.date,
                                                                     sector_destination=movi_entity.sector_destination,
                                                                     machining_batch=movi_entity.machining_batch,
                                                                     assembly_batch=movi_entity.assembly_batch
                                                                     )
                new_stock = self.repo.create_stock(scheme=entity)
                
                return new_stock
        except Exception as e:
            self.repo.session.rollback()