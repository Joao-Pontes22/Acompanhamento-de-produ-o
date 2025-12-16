from fastapi import APIRouter, Depends
from app.Services.Login_Service import login_service
from app.repositories.Employers_repositories import employersRepo
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.Dependecies import Init_Session, Verify_Token
from app.Schemes.Login_Scheme import Login_Scheme


Login_Router = APIRouter(prefix="/login", tags=["Login Operation"])


@Login_Router.post("/Login")
async def Login(scheme: Login_Scheme,session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    login  = service.service_login_in(scheme=scheme)
    return login

@Login_Router.post("/Login_Form")
async def login_form(login_info:OAuth2PasswordRequestForm = Depends(), session: Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    employer = service.service_login_form_in(scheme=login_info)
    return employer

@Login_Router.post("/Refresh_Token")
async def refresh_token(employer_id = Depends(Verify_Token), session:Session = Depends(Init_Session)):
    repo = employersRepo(session=session)
    service = login_service(repo=repo)
    token = service.service_refresh_token(employer_id=employer_id)
    return token