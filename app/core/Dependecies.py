from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from jose import jwt
from jose import JWTError
from app.models.Models import engine, Employers
from fastapi import Depends, HTTPException
from app.core.Settings.Settings import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.domain.Exceptions import NotFoundException
def Init_Session():
    Session = None
    try:
     Session = sessionmaker(bind=engine)
     session = Session()
     yield session
    except Exception:
       session.rollback()
       raise
    finally:
     session.close()
     print("Session closed.")

def Verify_Token (token = Depends(oauth2_scheme), session:Session = Depends(Init_Session) ):
    try:
        array_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        employer_id = array_info.get("sub")
    except JWTError:
        raise HTTPException (status_code=401, detail="Invalid token")
    employer = session.query(Employers).filter(Employers.ID == employer_id).first()
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return(employer_id)
  
