from datetime import datetime, timedelta, timezone
from app.Schemes.Login_Scheme import Login_Scheme
from fastapi import HTTPException
from app.core.Settings.Settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.Employers_repositories import employersRepo
class login_service:
    def __init__(self, repo:employersRepo):
        self.repo = repo

    def service_login_in(self, scheme:Login_Scheme):
        employer = self.repo.repo_find_by_id(id=scheme.id)
        if not employer:
            raise HTTPException(status_code=404, detail="Employer not foud")
        if not bcrypt_context.verify(scheme.password, employer.password):
            raise HTTPException(status_code=400, detail="Password incorrect")
        class_acces_token  = create_token(employerID=scheme.id)
        acces_token = class_acces_token.create_access_token()
        refresh_token= class_acces_token.create_refresh_token()
        return {"access_token": acces_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}
    
    def service_login_form_in(self, scheme:OAuth2PasswordRequestForm):
        employer = self.repo.repo_find_by_name(name=scheme.username)
        if not employer:
            raise HTTPException(status_code=404, detail="Employer not foud")
        if not bcrypt_context.verify(scheme.password, employer.password):
            raise HTTPException(status_code=400, detail="Password incorrect")
        class_acces_token  = create_token(employerID=employer.ID)
        access_token = class_acces_token.create_access_token()
        return {"access_token": access_token,
                "token_type": "bearer"}
    
    def service_refresh_token(self, employer_id:int):
        class_acces_token = create_token(employerID=employer_id)
        access_token = class_acces_token.create_access_token()
        return {"access_token": access_token,
                "token_type": "bearer"}
    
class create_token:
    def __init__(self, employerID):
        self.employerID = employerID

    def create_access_token(self):
        expiration_date = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        payload = {
            "sub": str(self.employerID),
            "type": "access",
            "exp": expiration_date,
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self):
        expiration_date = datetime.now(timezone.utc) + timedelta(days=7)

        payload = {
            "sub": str(self.employerID),
            "type": "refresh",
            "exp": expiration_date,
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        