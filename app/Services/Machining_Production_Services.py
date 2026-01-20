from app.repositories.Machining_Production_repository import Machining_ProductionRepository
from app.domain.Entitys.Machining_Production_entitys import MachiningProductionsEntity, MachiningProductionsEntityFiltred
from app.domain.Entitys.Stock_entitys import StockEntity
from app.Schemes.Machining_Production_Schemes import MachiningProductionScheme
from app.repositories.Relation_repository import RelationRepository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Machines_repository import MachineRepository
from app.repositories.Sectors_repository import SectorsRepository
from app.repositories.Stock_repository import StockRepository
from app.repositories.Movimentation_repository import MovimentationRepository
from app.domain.Exceptions import NotFoundException, AlreadyExist
from app.Services.Stock_Services import Stock_Services
from app.Schemes.Stock_Schemes import StockScheme, UpdateStockInfoScheme
class MachiningProductionServices:
    def __init__(self, Machining_Production_repo: Machining_ProductionRepository):
        self.Machining_Production_repo = Machining_Production_repo


    def create_machining_production(self, 
                                    Scheme:MachiningProductionScheme, 
                                    relation_repo: RelationRepository,
                                    sector_repo: SectorsRepository, 
                                    machine_repo: MachineRepository, 
                                    employer_repo: EmployersRepository,
                                    stock_repo: StockRepository,
                                    movimentation_repo: MovimentationRepository,
                                    stock_service: Stock_Services
                                    ):
        
        entity = MachiningProductionsEntity(sector_name=Scheme.sector_name,
                                           machine_name=Scheme.machine_name,
                                           date=Scheme.Date,
                                           duration_process=Scheme.duration_process,
                                           input_part_number=Scheme.input_part_number,
                                           output_part_number=Scheme.output_part_number,
                                           batch=Scheme.batch,
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
        
        employer = employer_repo.get_by_emp_id(emp_id=entity.emp_id)
        if not employer:
            raise NotFoundException("Employer")
        
        raw_stock = stock_repo.get_specify_stock(sector_name=entity.sector_name, 
                                                 part_number=entity.input_part_number, 
                                                 batch=entity.batch)
        if not raw_stock:
            raise NotFoundException("Stock raw component")

        machined_last_movimentation = movimentation_repo.get_movimentation_filtered_first(
            part_number=entity.output_part_number,
            origin=entity.sector_name,
            movimentation_type="CREATE",
            movimentation_id=True
        )
        if not machined_last_movimentation:
            stock_scheme = StockScheme(sector_name=entity.sector_name,
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
            stock_scheme = UpdateStockInfoScheme(
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
        machining_productions = self.Machining_Production_repo.get_machining_productions_filtered(sector_name=entity.sector_name,
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