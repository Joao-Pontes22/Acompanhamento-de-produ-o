from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Schemes.Responses.Response_Auth import Response_Auth
from app.Schemes.Employers_Schemes import Employers_Scheme, Employers_Scheme_Update
from app.core.Dependecies import Init_Session
from app.repositories.Employers_repositories import employersRepo
from app.Services.Employers_Services import Emp_services
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.repositories.Sectors_repositorie import Sectors_repositorie
Employer_Router = APIRouter(prefix="/Employers", tags=["Employers Operation"])

@Employer_Router.post("/Create_Employer")
async def Create_Employer(Auth_Data: Employers_Scheme,session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    sectors_repo = Sectors_repositorie(session=session)
    service = Emp_services(repo=repo)
    try:
        employer = service.post_employer(Auth_Data=Auth_Data, sectors_repo=sectors_repo)
        return {"message": "Employer created successful"}
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Employer_Router.get("/get_employers", response_model=list[Response_Auth])
async def get_employers(session: Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    try:
        employers = service.service_get_all_employers()
        return employers
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

@Employer_Router.get("/GET_Employer_By_Emp_ID/{emp_id}", response_model=Response_Auth)
async def get_emploer_by_emp_id(emp_id:str, session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    try:
        employer = service.service_get_employer_by_emp_id(emp_id=emp_id)
        return employer
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))



@Employer_Router.delete("/Delete_employer/{id}")
async def delete_employer (id:int, session:Session=Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    try:
        delete = service.delete_employer(ID=id)
        return {"message": "Employer deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@Employer_Router.get("/Get_employer_by_id/{id}", response_model=Response_Auth)
async def get_by_id(id:int, session:Session=Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = Emp_services(repo=repo)
    try:
        employer = service.service_get_employer_by_id(employer_id=id)
        return employer
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))