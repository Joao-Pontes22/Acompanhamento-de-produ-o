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
#---------------------// AUTH OPERATIONS //---------------------#
class Emp_services:
     def __init__(self, repo: employersRepo):
          self.repo = repo

     def service_get_employer_by_emp_id(self, emp_id: str):
          employer = self.repo.repo_find_by_emp_id(emp_id= emp_id)
          if not employer:
               raise NotFoundException(entity="Employer")
          return employer

     def service_get_employer_by_id(self, employer_id: int):
          employer = self.repo.repo_find_by_id(id= employer_id)
          if not employer:
               raise NotFoundException(entity="Employer")

          return employer

     def service_get_all_employers(self):
          employers = self.repo.repo_get_all_employers()
          if not employers:
               raise NotFoundException(entity="Employers")
          return employers
     
     def post_employer(self, Auth_Data: Employers_Scheme, sectors_repo: Sectors_repositorie):
          employer = self.repo.repo_find_by_emp_id(emp_id=Auth_Data.emp_id)
          if employer:
               raise AlreadyExist(entity="Employer")
          sector = sectors_repo.repo_get_sector_by_id(id=Auth_Data.sector_ID)
          if not sector:
               raise NotFoundException(entity="Sector")
          hashed_password = bcrypt_context.hash(Auth_Data.password)
          new_employer = self.repo.repo_create_employer(name=Auth_Data.name,
                                             sector_id=Auth_Data.sector_ID,
                                             password=hashed_password,
                                             emp_id=Auth_Data.emp_id)
          return new_employer

     def delete_employer(self, ID:int):
          employer = self.repo.repo_find_by_id(id=ID)
          if not employer:
               raise NotFoundException(entity="Employer")
          delete = self.repo.repo_delete_employer(employer=employer)
          return delete

