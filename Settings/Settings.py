import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi import Depends
from Dependecies import Init_Session
from Models.Models import Employers, Sectors
import os
from Schemes.Auth_Schemes import Auth_Scheme
from datetime import datetime, timedelta, timezone
load_dotenv()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


#---------------------// AUTH OPERATIONS //---------------------#
async def get_employer_name(name: str, session: Session = Depends(Init_Session)):
     employer = session.query(Employers).filter(Employers.name == name.upper()).first()
     return employer
    
async def post_employer(Auth_Data: Auth_Scheme, session: Session =Depends(Init_Session)):
     hashed_password = bcrypt_context.hash(Auth_Data.password)
     employer = Employers(name=Auth_Data.name.upper(), password=hashed_password, sector=Auth_Data.sector_ID)
     session.add(employer)
     session.commit()
     return employer

#---------------------// SECTOR OPERATIONS //---------------------#
async def get_sectors(session: Session = Depends(Init_Session)):
    sectors = session.query(Sectors).all()
    result = []
    for sector in sectors:
        result.append({
            "ID": sector.ID,
            "sector": sector.sector,
            "tag": sector.tag
        })
    return result

#---------------------// TOKEN OPERATIONS //---------------------#
def create_access_token(employer_ID: int, token_duration: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + token_duration
    array_info = {"sub": str(employer_ID),
                  "exp": expiration_date
                  }
    token = jwt.encode(array_info, SECRET_KEY, algorithm=ALGORITHM)
    return token