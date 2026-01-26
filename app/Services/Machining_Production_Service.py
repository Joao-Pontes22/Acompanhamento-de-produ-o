#Repository
from app.repositories.Machining_Production_repository import Machining_ProductionRepository
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Stock_repository import StockRepository
from app.repositories.Movimentation_repository import MovimentationRepository
#Entity
from app.domain.Entitys.Machining_Production_entitys import MachiningProductionsEntity, MachiningProductionsEntityFiltred
#Schema
from app.Schemas.Machining_Production_Schemas import MachiningProductionSchema
from app.Schemas.Stock_Schemas import StockSchema, UpdateStockInfoSchema
#Exceptions
from app.domain.Exceptions import NotFoundException
#Service
from app.Services.Stock_Service import StockService

class MachiningProductionServices:
    def __init__(self, Machining_Production_repo: Machining_ProductionRepository):
        self.Machining_Production_repo = Machining_Production_repo


    def create_machining_production(self, 
                                    Scheme:MachiningProductionSchema, 
                                    relation_repo: RelationRepository,
                                    sector_repo: SectorsRepository, 
                                    machine_repo: MachineRepository, 
                                    employer_repo: EmployersRepository,
                                    stock_repo: StockRepository,
                                    movimentation_repo: MovimentationRepository,
                                    stock_service: StockService
                                    ):
        
        entity = MachiningProductionsEntity(sector_name=Scheme.sector_name,
                                           machine_name=Scheme.machine_name,
                                           date=Scheme.Date,
                                           duration_process=Scheme.duration_process,
                                           input_part_number=Scheme.input_part_number,
                                           output_part_number=Scheme.output_part_number,
                                           setup=Scheme.setup,
                                           emp_id=Scheme.emp_id,
                                           status=Scheme.status
                                           )

        serial_id = self.create_serial_id(part_number=entity.output_part_number)

        relation = relation_repo.get_relations_filtred_first(create_item_part_number=entity.output_part_number, 
                                                             consume_item_part_number=entity.input_part_number
                                                             )
        if not relation:
            raise NotFoundException("Raw Component")
        
        sector = sector_repo.get_sector_by_name(name=entity.sector_name)
        if not sector:
            raise NotFoundException("Sector")
        
        machine = machine_repo.get_machine_filtred_first(machine=entity.machine_name)
        if not machine:
            raise NotFoundException("Machine")
        
        employer = employer_repo.get_employer_filtred(emp_id=entity.emp_id)
        if not employer:
            raise NotFoundException("Employer")
        
        raw_stock = stock_repo.get_filtred_stock(sector_name=entity.sector_name, 
                                                 part_number=entity.input_part_number, 
                                                 setup=entity.setup)
        if not raw_stock:
            raise NotFoundException("Stock raw component")

        machined_last_movimentation = movimentation_repo.get_movimentation_create_stock_filtred_first(
            part_number=entity.output_part_number,
            origin=entity.sector_name,
            movimentation_id=True
        )
        if not machined_last_movimentation:
            stock_scheme = StockSchema(sector_name=entity.sector_name,
                                        part_number=entity.output_part_number,
                                        qnty=1,
                                        reason="Machining Production Creation")
            
            stock = stock_service.create_stock(scheme=stock_scheme, 
                                               employer_id=entity.emp_id
                                               )
            
            machining_production = self.Machining_Production_repo.create_machining_production(sector_name=entity.sector_name,
                                                                                             machine_name=entity.machine_name,
                                                                                             date=entity.date,
                                                                                             duration_process=entity.duration_process,
                                                                                             input_part_number=entity.input_part_number,
                                                                                             output_part_number=entity.output_part_number,
                                                                                             batch=entity.batch,
                                                                                             emp_id=entity.emp_id,
                                                                                             status=entity.status,
                                                                                             serial_id=serial_id
                                                                                             )
            return machining_production
        else:
            stock_scheme = UpdateStockInfoSchema(
                                        qnty=machined_last_movimentation.qnty + 1)
            stock = stock_service.update_stock(scheme=stock_scheme, 
                                                employer_id=entity.emp_id)
            machining_production = self.Machining_Production_repo.create_machining_production(sector_name=entity.sector_name,
                                                                                              machine_name=entity.machine_name,
                                                                                              date=entity.date,
                                                                                              duration_process=entity.duration_process,
                                                                                              input_part_number=entity.input_part_number,
                                                                                              output_part_number=entity.output_part_number,
                                                                                              batch=entity.batch,
                                                                                              emp_id=entity.emp_id,
                                                                                              status=entity.status,
                                                                                              serial_id=serial_id)
            return machining_production
        
    def service_get_all_machining_production(self):
        machining_productions = self.Machining_Production_repo.get_all_machining_production()
        return machining_productions
    
    def service_get_machining_productions_filtred_first(self, sector_name: str, 
                                                        machine_name: str,
                                                        batch: str,
                                                        machining_batch: str,
                                                        date: str,
                                                        input_part_number: str,
                                                        output_part_number: str,
                                                        emp_id_employer: str,
                                                        status: str
                                                        ):
        
        entity = MachiningProductionsEntityFiltred(sector_name=sector_name,
                                                 machine_name=machine_name,
                                                 batch=batch,
                                                 machining_batch=machining_batch,
                                                 Date=date,
                                                 input_part_number=input_part_number,
                                                 output_part_number=output_part_number,
                                                 emp_id_employer=emp_id_employer,
                                                 status=status
                                                 )
        
        machining_productions = self.Machining_Production_repo.get_machining_productions_filtred(sector_name=entity.sector_name,
                                                                                                  machine_name=entity.machine_name,
                                                                                                  batch=entity.batch,
                                                                                                  input_part_number=entity.input_part_number,
                                                                                                  output_part_number=entity.output_part_number,
                                                                                                  emp_id_employer=entity.emp_id_employer,
                                                                                                  status=entity.status)
        return machining_productions

    def create_serial_id(self, part_number: str):
        last_id = self.service_get_machining_productions_filtred_first(output_part_number=part_number)
        if not last_id:
            return 1
        return last_id.serial_ID + 1