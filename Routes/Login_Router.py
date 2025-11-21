from fastapi import APIRouter, Depends, HTTPException
from Settings.Settings import get_employer_name,bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from Settings.Settings import create_access_token
from jose import jwt
from Models.Models import Employers
from sqlalchemy.orm import Session
from Dependecies import Init_Session
from Schemes.Login_Scheme import Login_Scheme
from datetime import datetime, timedelta, timezone

Login_Router = APIRouter(prefix="/login", tags=["Login"])


@Login_Router.post("/Login")
async def login(Login_Scheme: Login_Scheme,session:Session = Depends(Init_Session)):
    employer= await get_employer_name(name=Login_Scheme.name, session=session)
    if not employer:
        raise HTTPException(status_code=400, detail="Employer not found")
    if not bcrypt_context.verify(Login_Scheme.password, employer.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if employer and bcrypt_context.verify(Login_Scheme.password, employer.password):
        access_token = create_access_token(employer_ID=employer.ID,token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_access_token(employer_ID=employer.ID, token_duration=timedelta(days=7))
        return {"Access_token": access_token,
                "Refresh_token": refresh_token}