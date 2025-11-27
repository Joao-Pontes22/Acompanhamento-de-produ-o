import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from Settings.Settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from Dependecies import Init_Session
from Models.Models import Employers
from Schemes.Auth_Schemes import Auth_Scheme
from datetime import datetime, timedelta, timezone
from Services.Sector_Service import get_sectors


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

#---------------------// AUTH OPERATIONS //---------------------#
async def get_employer_name(name: str, session: Session = Depends(Init_Session)):
     employer = session.query(Employers).filter(Employers.name == name.upper()).first()
     return employer
async def get_employer_id(employer_id: int, session: Session = Depends(Init_Session)):
     employer = session.query(Employers).filter(Employers.ID == employer_id).first()
     return employer

async def get_all_employers(session: Session = Depends(Init_Session)):
     employers = session.query(Employers).all()
     return employers
    
async def post_employer(Auth_Data: Auth_Scheme, session: Session =Depends(Init_Session)):
     hashed_password = bcrypt_context.hash(Auth_Data.password)
     employer = Employers(name=Auth_Data.name.upper(), password=hashed_password, sector=Auth_Data.sector_ID)
     sectors = await get_sectors(session=session)
     sector_ids = []
     for sector in sectors:
        sector_ids.append(sector.ID)
     if employer.sector_ID not in sector_ids:
        raise HTTPException(status_code=400, detail="Sector ID does not exist")
     session.add(employer)
     session.commit()
     return employer
#---------------------// TOKEN OPERATIONS //---------------------#
def create_access_token(employer_ID: int, token_duration: timedelta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))):
    expiration_date = datetime.now(timezone.utc) + token_duration
    array_info = {"sub": str(employer_ID),
                  "exp": expiration_date
                  }
    token = jwt.encode(array_info, SECRET_KEY, algorithm=ALGORITHM)
    return token