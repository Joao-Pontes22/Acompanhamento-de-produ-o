#FASTAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas and Response
from app.Schemas.Responses.Response_Auth import ResponseAuth
from app.Schemas.Employers_Schemas import EmployersSchema, UpdateEmployersInfoSchema
from app.core.Dependecies import Init_Session
from app.repositories.Employers_repository import EmployersRepository
from app.Services.Employers_Service import EmployersServices
from app.domain.Exceptions import AlreadyExist, NotFoundException
from app.repositories.Sectors_repository import SectorsRepository


Employer_Router = APIRouter(prefix="/Employers", tags=["Employers Operation"])

@Employer_Router.post("/create_Employer")
async def Create_Employer(scheme: EmployersSchema,
                          session:Session = Depends(Init_Session)
                          ):
    
    repo = EmployersRepository(session=session)
    sectors_repo = SectorsRepository(session=session)
    service = EmployersServices(repo=repo)

    try:
        employer = service.post_employer(scheme=scheme, sectors_repo=sectors_repo)

        return {"message": "Employer created successful"}
    
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Employer_Router.get("/get_employers", 
                     response_model=list[ResponseAuth]
                     )
async def get_employers(session: Session = Depends(Init_Session)):

    repo = EmployersRepository(session=session)
    service = EmployersServices(repo=repo)

    try:
        employers = service.get_all_employers()

        return employers
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Employer_Router.get("/get_employer_by_emp_id/{emp_id}", 
                     response_model=ResponseAuth
                     )
async def get_emploer_by_emp_id(emp_id:str, 
                                session:Session = Depends(Init_Session)
                                ):

    repo = EmployersRepository(session=session)
    service = EmployersServices(repo=repo)

    try:

        employer = service.get_employer_by_emp_id(emp_id=emp_id)

        return employer
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))



@Employer_Router.delete("/Delete_employer/{emp_id}")
async def delete_employer (emp_id:str, 
                           session:Session=Depends(Init_Session)
                           ):
    
    repo = EmployersRepository(session=session)
    service = EmployersServices(repo=repo)

    try:

        delete = service.delete_employer(emp_id=emp_id)

        return {"message": "Employer deleted successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    