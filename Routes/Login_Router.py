from fastapi import APIRouter, Depends, HTTPException
from Services.Auth_Services import get_employer_name,bcrypt_context
from Services.Auth_Services import create_access_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from Dependecies import Init_Session, Verify_Token
from Schemes.Login_Scheme import Login_Scheme
from datetime import timedelta
Login_Router = APIRouter(prefix="/login", tags=["Login"])


@Login_Router.post("/Login")
async def login(Login_Scheme: Login_Scheme,session:Session = Depends(Init_Session)):
    employer = await get_employer_name(name=Login_Scheme.name, session=session)
    if not employer:
        raise HTTPException(status_code=400, detail="Employer not found")
    if not bcrypt_context.verify(Login_Scheme.password, employer.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if employer and bcrypt_context.verify(Login_Scheme.password, employer.password):
        access_token = create_access_token(employer_ID=employer.ID)
        refresh_token = create_access_token(employer_ID=employer.ID, token_duration=timedelta(days=7))
        return {"Access_token": access_token,
                "Refresh_token": refresh_token}

@Login_Router.post("/Login_Form")
async def login_form(form_info: OAuth2PasswordRequestForm = Depends(), 
                     session: Session = Depends(Init_Session)
                     ):
    employer = await get_employer_name(name=form_info.username.upper(), 
                                       session=session
                                       )
    if not employer:
        raise HTTPException(status_code=400, detail="Employer not found")
    if not bcrypt_context.verify(form_info.password, employer.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if employer and bcrypt_context.verify(form_info.password, 
                                          employer.password
                                          ):
        access_token = create_access_token(employer_ID=employer.ID)
        return {"access_token": access_token,
                "token_type": "bearer"}
        

@Login_Router.post("/Refresh_Token")
async def refresh_token(employer_id: str = Depends(Verify_Token)):  
      new_acces_token = create_access_token(employer_ID=employer_id)
      return {"Acces_token:": new_acces_token,
              "token_type": "bearer"}
    