from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Schemes.Responses.Response_Auth import Response_Auth
from app.Schemes.Employers_Schemes import Employers_Scheme, Employers_Scheme_Update
from app.core.Dependecies import Init_Session
from app.repositories.Employers_repositories import employersRepo
from app.Services.Employers_Services import Emp_services


Employer_Router = APIRouter(prefix="/Employers", tags=["Employers Operation"])

@Employer_Router.get("/get_employers")
async def get_employers(session: Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    employers = service.service_get_all_employers()
    return employers

@Employer_Router.get("/GET_Employer_By_Name/{name}", response_model=Response_Auth)
async def get_emploer_by_name(name:str, session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    employer = service.service_get_employer_by_name(name=name)
    return employer

@Employer_Router.post("/Create_Employer")
async def Create_Employer(Auth_Data: Employers_Scheme,session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    employer = service.post_employer(Auth_Data=Auth_Data)
    return {"message": "Employer created successful"}

@Employer_Router.delete("/Delete_employer", response_model=Response_Auth)
async def delete_employer (id:int, session:Session=Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    delete = service.delete_employer(ID=id)
    return {"message": "Employer deleted successfuly",
            "Employer": delete}

@Employer_Router.get("Get_employer_by_{id}")
async def get_by_id(id:int, session:Session=Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    employer = service.service_get_employer_by_id(employer_id=id)
    return employer