from app.core.Settings.Settings import  bcrypt_context
from app.Schemes.Employers_Schemes import EmployersScheme, UpdateEmployersInfoScheme
from app.domain.Entitys.Employers_entitys import EmployersEntity
from app.repositories.Employers_repository import EmployersRepository
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.repositories.Sectors_repository import SectorsRepository
#---------------------// AUTH OPERATIONS //---------------------#
class EmployersServices:
     def __init__(self, repo: EmployersRepository):
          self.repo = repo

     
     def post_employer(self, 
                       scheme: EmployersScheme, 
                       sectors_repo: SectorsRepository
                       ):
          entity = EmployersEntity(name=scheme.name,
                                    sector_name=scheme.sector_name,
                                    emp_id=scheme.emp_id,
                                    password=scheme.password
                                    )
          
          employer = self.repo.get_by_emp_id(emp_id=entity.emp_id)
          if employer:
               raise AlreadyExist(entity="Employer")
          
          sector = sectors_repo.get_sector_by_name(name=entity.sector_name)
          if not sector:
               raise NotFoundException(entity="Sector")
          
          
          hashed_password = bcrypt_context.hash(entity.password)
          new_employer = self.repo.create_employer(name=entity.name,
                                             sector=entity.sector_name,
                                             password=hashed_password,
                                             emp_id=entity.emp_id)
          return new_employer
     

     def get_employer_by_emp_id(self, emp_id: str):

          employer = self.repo.get_by_emp_id(emp_id= emp_id)

          if not employer:
               raise NotFoundException(entity="Employer")
          
          return employer

     def get_all_employers(self):

          employers = self.repo.get_all_employers()

          if not employers:
               raise NotFoundException(entity="Employers")
          return employers
     
     

     def delete_employer(self, emp_id:str):

          employer = self.repo.get_by_emp_id(emp_id=emp_id)

          if not employer:
               raise NotFoundException(entity="Employer")
          
          delete = self.repo.delete_employer(employer=employer)
          return delete

