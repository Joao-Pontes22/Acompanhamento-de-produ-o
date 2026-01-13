import hashlib
from fastapi import Depends, HTTPException
from app.core.Settings.Settings import  bcrypt_context
from app.core.Dependecies import Init_Session
from app.models.Models import Employers
from app.Schemes.Employers_Schemes import Employers_Scheme, Employers_Scheme_Update
from datetime import datetime, timedelta, timezone
from app.domain.Value_objects.Name import value_Name
from app.domain.Entitys.Employers_entitys import employers_entity
from app.repositories.Employers_repositories import employersRepo
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.repositories.Sectors_repositorie import Sectors_repositorie
from app.domain.Value_objects import Sector
#---------------------// AUTH OPERATIONS //---------------------#
class Emp_services:
     def __init__(self, repo: employersRepo):
          self.repo = repo

     def service_get_employer_by_emp_id(self, emp_id: str):
          employer = self.repo.repo_find_by_emp_id(emp_id= emp_id)
          if not employer:
               raise NotFoundException(entity="Employer")
          return employer

     def service_get_all_employers(self):
          employers = self.repo.repo_get_all_employers()
          if not employers:
               raise NotFoundException(entity="Employers")
          return employers
     
     def post_employer(self, scheme: Employers_Scheme, sectors_repo: Sectors_repositorie):
          employer = self.repo.repo_find_by_emp_id(emp_id=scheme.emp_id)
          if employer:
               raise AlreadyExist(entity="Employer")
          entity = employers_entity(name=scheme.name,
                                    sector=scheme.sector,
                                    emp_id=scheme.emp_id,
                                    password=scheme.password)
          sector = sectors_repo.repo_get_sector_by_name(name=entity.sector)
          if not sector:
               raise NotFoundException(entity="Sector")
          hashed_password = bcrypt_context.hash(entity.password)
          new_employer = self.repo.repo_create_employer(name=entity.name,
                                             sector=entity.sector,
                                             password=hashed_password,
                                             emp_id=entity.emp_id)
          return new_employer

     def delete_employer(self, emp_id:str):
          employer = self.repo.repo_find_by_emp_id(emp_id=emp_id)
          if not employer:
               raise NotFoundException(entity="Employer")
          delete = self.repo.repo_delete_employer(employer=employer)
          return delete

