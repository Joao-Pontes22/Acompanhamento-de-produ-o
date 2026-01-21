#FastAPI
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
#Service
from app.Services.Login_Service import LoginService
#Repository
from app.repositories.Employers_repository import EmployersRepository
#SQLAlchemy
from sqlalchemy.orm import Session
#Dependecies
from app.core.Dependecies import Init_Session, Verify_Token
#Schema
from app.Schemas.Login_Schema import LoginSchema
#Exceptions
from app.domain.Exceptions import NotFoundException, IncorrectPasswordException


Login_Router = APIRouter(prefix="/Login", tags=["Login Operation"])


@Login_Router.post("/login")
async def Login(scheme: LoginSchema,
                session:Session = Depends(Init_Session)
                ):

    repo = EmployersRepository(session=session)
    service = LoginService(repo=repo)

    try:
        login  = service.login_in(scheme=scheme)

        return login
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordException as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@Login_Router.post("/login_Form")
async def login_form(login_info:OAuth2PasswordRequestForm = Depends(), 
                     session: Session = Depends(Init_Session)
                     ):
    
    repo = EmployersRepository(session=session)
    service = LoginService(repo=repo)

    try:

        employer = service.login_form_in(scheme=login_info)

        return employer
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Login_Router.post("/refresh_Token/{employer_id}")
async def refresh_token(employer_id = Depends(Verify_Token), 
                        session:Session = Depends(Init_Session)
                        ):
    
    repo = EmployersRepository(session=session)
    service = LoginService(repo=repo)
    try:

        token = service.refresh_token(employer_id=employer_id)

        return token
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    