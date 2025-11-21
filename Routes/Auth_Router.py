from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Schemes.Auth_Schemes import Auth_Scheme
from Settings.Settings import post_employer
from Dependecies import Init_Session
Auth_Router = APIRouter(prefix="/auth", tags=["Authentication"])

@Auth_Router.post("/Create_User")
async def create_user(Auth_Data: Auth_Scheme, session: Session = Depends(Init_Session)):
    new_employer = await post_employer(Auth_Data=Auth_Data, session=session)
    return {"message": "User created successfully", "name": new_employer.name}