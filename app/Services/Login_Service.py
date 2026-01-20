from datetime import datetime, timedelta, timezone
from app.Schemes.Login_Scheme import LoginScheme
from app.core.Settings.Settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.Employers_repository import EmployersRepository
from app.domain.Exceptions import NotFoundException, IncorrectPasswordException

class loginService:
    def __init__(self, repo:EmployersRepository):
        self.repo = repo

    def service_login_in(self, scheme:LoginScheme):

        employer = self.repo.get_by_emp_id(emp_id=scheme.emp_id)
        if not employer:
            raise NotFoundException("Employer")
        
        if not bcrypt_context.verify(scheme.password, employer.password):
            raise IncorrectPasswordException()
        
        class_acces_token  = create_token(employerID=employer.ID)

        acces_token = class_acces_token.create_access_token()
        refresh_token= class_acces_token.create_refresh_token()

        return {"access_token": acces_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"}
    
    def service_login_form_in(self, scheme:OAuth2PasswordRequestForm):

        employer = self.repo.get_by_emp_id(emp_id=scheme.username)
        if not employer:
            raise NotFoundException("Employer")
        
        if not bcrypt_context.verify(scheme.password, employer.password):
            raise IncorrectPasswordException()
        
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

        