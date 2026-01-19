from app.repositories.Machining_Production_repositorie import Machining_ProductionRepositorie
from app.domain.Entitys.Machining_Production_entitys import MachiningProductionEntity, MachiningProductionEntityFiltred
from app.domain.Entitys.Stock_entitys import Stock_Entity_Machined
from app.Schemes.Machining_Production_Schemes import Machining_Production_Scheme
from app.repositories.Relation_repositorie import Relation_repositorie
from app.repositories.Employers_repositories import employersRepo
from app.repositories.Machines_repositorie import Machine_Repositorie
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.repositories.Stock_repositorie import Stock_repositorie
from app.repositories.Movimentation_repositorie import MovimentationRepository

from app.domain.Exceptions import NotFoundException, AlreadyExist

from app.Services.Stock_Services import Stock_Services
from app.Schemes.Stock_Schemes import Stock_Scheme
class MachiningProductionServices:
    def __init__(self, Machining_Production_repo: Machining_ProductionRepositorie):
        self.Machining_Production_repo = Machining_Production_repo


    def service_create_machining_production(self, Scheme:Machining_Production_Scheme, 
                                            relation_repo: Relation_repositorie,
                                             sector_repo: Sectors_repositorie, 
                                             machine_repo: Machine_Repositorie, 
                                             employer_repo: employersRepo,
                                             stock_repo: Stock_repositorie,
                                             movimentation_repo: MovimentationRepository,
                                                stock_service: Stock_Services
                                             ):
        print(Scheme)
        entity = MachiningProductionEntity(scheme=Scheme)
        print(entity)
        serial_id = self.create_serial_id(part_number=entity.output_part_number)
        relation = relation_repo.get_relations_filtred_first(create_item_part_number=entity.output_part_number, consume_item_part_number=entity.input_part_number)
        if not relation:
            raise NotFoundException("Raw Component")
        sector = sector_repo.repo_get_sector_by_name(entity.sector_name)
        if not sector:
            raise NotFoundException("Sector")
        machine = machine_repo.get_machine_filtred(machine=entity.machine_name)
        if not machine:
            raise NotFoundException("Machine")
        employer = employer_repo.repo_find_by_emp_id(entity.emp_id_employer)
        if not employer:
            raise NotFoundException("Employer")
        raw_stock = stock_repo.get_specify_stock(sector_name=entity.sector_name, 
                                                 part_number=entity.input_part_number, 
                                                 batch=entity.batch)
        if not raw_stock:
            raise NotFoundException("Stock raw component")

        machined_stock = movimentation_repo.get_movimentation_filtered_first(
            part_number=entity.output_part_number,
            origin=entity.sector_name,
            movimentation_type="CREATE",
            movimentation_id=True
        )
        if not machined_stock:
            stock_scheme = Stock_Scheme(sector=entity.sector_name,
                                        part_number=entity.output_part_number,
                                        qnty=1,
                                        reason="Machining Production Creation")
            
            stock = stock_service.Service_Create_Stock(scheme=stock_scheme, employer_id=entity.emp_id_employer)
            machining_production = self.Machining_Production_repo.repo_create_machining_production(Scheme=entity)
            return machining_production
        else:
            stock_scheme = Stock_Scheme(
                                        qnty=machined_stock.qnty + 1)
            stock = stock_service.Service_update_stock(scheme=stock_scheme, 
                                                      employer_id=entity.emp_id_employer)
            machining_production = self.Machining_Production_repo.repo_create_machining_production(Scheme=entity, serial_id=serial_id)
            return machining_production
        
    def service_get_all_machining_production(self):
        machining_productions = self.Machining_Production_repo.repo_get_all_machining_production()
        return machining_productions
    
    def service_get_machining_productions_filtred_first(self, sector_name: str = None, 
                                                  machine_name: str = None,
                                                  batch: str = None,
                                                  machining_batch: str = None,
                                                  Date: str = None,
                                                    input_part_number: str = None,
                                                    output_part_number: str = None,
                                                    emp_id_employer: str = None,
                                                    status: str = None
                                                ):
        entity = MachiningProductionEntityFiltred(sector_name=sector_name,
                                                 machine_name=machine_name,
                                                 batch=batch,
                                                 machining_batch=machining_batch,
                                                 Date=Date,
                                                 input_part_number=input_part_number,
                                                 output_part_number=output_part_number,
                                                 emp_id_employer=emp_id_employer,
                                                 status=status)
        machining_productions = self.Machining_Production_repo.repo_get_machining_procutions_filtred(sector_name=entity.sector_name,
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