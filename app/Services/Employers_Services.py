from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.core.Settings.Settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, bcrypt_context
from app.core.Dependecies import Init_Session
from app.models.Models import Employers
from app.Schemes.Employers_Schemes import Employers_Scheme, Employers_Scheme_Update
from datetime import datetime, timedelta, timezone
from app.domain.Value_objects.Name import value_Name
from app.domain.Entitys.Employers_entitys import employers_entity
from app.repositories.Employers_repositories import employersRepo

#---------------------// AUTH OPERATIONS //---------------------#
class Emp_services:
     def __init__(self, repo):
          self.repo = repo

     def service_get_employer_by_name(self, name: str):
          employer_name = value_Name(name=name)
          employer = self.repo.repo_find_by_name(employer_name.name)
          if not employer:
               raise HTTPException(status_code=404, detail="Employer do not found")
          return {"Id": employer.ID,
                  "Name": employer.name,
                  "Sector": employer.employer_sector.sector,
                  "Tag sector": employer.employer_sector.tag}

     def service_get_employer_by_id(self, employer_id: int):
          employer = self.repo.repo_find_by_id(id= employer_id)
          if not employer:
               raise HTTPException(status_code=404, detail="Employer do not found")

          return {"Id": employer.ID,
                  "Name": employer.name,
                  "Sector": employer.employer_sector.sector,
                  "Tag sector": employer.employer_sector.tag}

     def service_get_all_employers(self):
          employers = self.repo.repo_get_all_employers()
          if not employers:
               raise HTTPException(status_code=401, detail="Do not have employerrs yet")
          return [
               {"Id": emp.ID,
                  "Name": emp.name,
                  "Sector": emp.employer_sector.sector,
                  "Tag sector": emp.employer_sector.tag}
                  for emp in employers
                  ]
     
     def post_employer(self, Auth_Data: Employers_Scheme):
          hashed_password = bcrypt_context.hash(Auth_Data.password)
          new_employer = self.repo.repo_create_employer(name=Auth_Data.name,
                                             sector_id=Auth_Data.sector_ID,
                                             password=hashed_password)
          return {"Id": new_employer.ID,
                  "Name": new_employer.name,
                  "Sector": new_employer.employer_sector.sector,
                  "Tag sector": new_employer.employer_sector.tag}

     def delete_employer(self, ID:int):
          employer = self.repo.repo_find_by_id(id=ID)
          if not employer:
               raise HTTPException(status_code=401, detail="Employer not found")
          delete = self.repo.repo_delete_employer(employer=employer)
          return delete

