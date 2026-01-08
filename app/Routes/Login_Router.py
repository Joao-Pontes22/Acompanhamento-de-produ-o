from fastapi import APIRouter, Depends, HTTPException
from app.Services.Login_Service import login_service
from app.repositories.Employers_repositories import employersRepo
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.Dependecies import Init_Session, Verify_Token
from app.Schemes.Login_Scheme import Login_Scheme
from app.domain.Exceptions import NotFoundException, IncorrectPasswordException

Login_Router = APIRouter(prefix="/Login", tags=["Login Operation"])


@Login_Router.post("/Login")
async def Login(scheme: Login_Scheme,session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    try:
        login  = service.service_login_in(scheme=scheme)
        return login
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordException as e:
        raise HTTPException(status_code=400, detail=str(e))
@Login_Router.post("/Login_Form")
async def login_form(login_info:OAuth2PasswordRequestForm = Depends(), session: Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    try:
        employer = service.service_login_form_in(scheme=login_info)
        return employer
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordException as e:
        raise HTTPException(status_code=400, detail=str(e))

@Login_Router.post("/Refresh_Token/{employer_id}")
async def refresh_token(employer_id = Depends(Verify_Token), session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    try:
        token = service.service_refresh_token(employer_id=employer_id)
        return token
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    