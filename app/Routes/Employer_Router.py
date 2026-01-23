#FASTAPI
from fastapi import APIRouter, Depends, HTTPException
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas
from app.Schemas.Responses.Response_Auth import ResponseAuth
from app.Schemas.Employers_Schemas import EmployersSchema, UpdateEmployersInfoSchema
from app.Schemas.Queries.employer_query_params import EmployersParameters
#Dependecies
from app.core.Dependecies import Init_Session
#Repository
from app.repositories.Employers_repository import EmployersRepository
from app.repositories.Sectors_repository import SectorsRepository
#Service
from app.Services.Employers_Service import EmployersServices
#Exceptions
from app.domain.Exceptions import AlreadyExist, NotFoundException


Employer_Router = APIRouter(prefix="/Employers", tags=["Employers Operation"])

@Employer_Router.post("/create_employer")
async def Create_Employer(body: EmployersSchema,
                          session:Session = Depends(Init_Session)
                          ):
    
    repo = EmployersRepository(session=session)
    sectors_repo = SectorsRepository(session=session)
    service = EmployersServices(repo=repo)

    try:
        employer = service.post_employer(scheme=body, 
                                         sectors_repo=sectors_repo)

        return {"message": "Employer created successfuly"}
    
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


@Employer_Router.get("/get_employer_filtred", 
                     response_model=list[ResponseAuth]
                     )
async def get_employers_filtred(query_params: EmployersParameters = Depends(), 
                                session:Session = Depends(Init_Session)
                                ):

    repo = EmployersRepository(session=session)
    service = EmployersServices(repo=repo)

    try:

        employer = service.get_employer_filtred(query_params=query_params)

        return employer
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))



@Employer_Router.delete("/delete_employer/{emp_id}")
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
    