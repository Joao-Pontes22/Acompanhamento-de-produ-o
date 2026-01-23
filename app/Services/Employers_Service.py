#Crypt_Context
from app.core.Settings.Settings import  bcrypt_context
#Schemas
from app.Schemas.Employers_Schemas import EmployersSchema, UpdateEmployersInfoSchema
#Entity
from app.domain.Entitys.Employers_entitys import EmployersEntity
#Repository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Sectors_repository import SectorsRepository
#Exceptions
from app.domain.Exceptions import AlreadyExist, NotFoundException
#Value_Object
from app.domain.Value_objects.Emp_id import ValueEmpID

#---------------------// AUTH OPERATIONS //---------------------#
class EmployersServices:
     def __init__(self, repo: EmployersRepository):
          self.repo = repo

     
     def post_employer(self, 
                       scheme: EmployersSchema, 
                       sectors_repo: SectorsRepository
                       ):
          entity = EmployersEntity(name=scheme.name,
                                    sector_name=scheme.sector_name,
                                    emp_id=scheme.emp_id,
                                    password=scheme.password
                                    )
          
          employer = self.repo.get_employer_filtred(emp_id=entity.emp_id)
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
     

     def get_employer_filtred(self, query_params: str):
          employer = self.repo.get_employer_filtred(emp_id= query_params.emp_id)

          if not employer:
               raise NotFoundException(entity="Employer")
          
          return employer

     def get_all_employers(self):

          employers = self.repo.get_all_employers()

          if not employers:
               raise NotFoundException(entity="Employers")
          return employers
     
     

     def delete_employer(self, emp_id:str):
          value_emp_id = ValueEmpID(emp_id=emp_id)
          employer = self.repo.get_employer_filtred(emp_id=value_emp_id.emp_id)

          if not employer:
               raise NotFoundException(entity="Employer")
          
          delete = self.repo.delete_employer(employer=employer)
          return delete

