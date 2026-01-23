from app.models.Employers import Employers
from typing import Optional

class EmployersRepository:
    def __init__(self,session):
        self.session = session

    def create_employer(self, name, sector, password, emp_id):
        new_employer = Employers(name=name,
                                 password=password,
                                 sector_name=sector,
                                 emp_id=emp_id)
        self.session.add(new_employer)
        self.session.commit()
        return new_employer
    
    def get_all_employers(self):
        employers = self.session.query(Employers).all()
        return employers
    
    def get_employer_filtred(self, 
                             id: Optional[int] = None,
                             name: Optional[str] = None,
                             emp_id: Optional[str] = None):
        
        query = self.session.query(Employers)
        if id:
            query = query.filter(Employers.ID == id)
        if name:
            query = query.filter(Employers.name == name)
        if emp_id:
            query = query.filter(Employers.emp_id == emp_id)
        return query.all()
    
    
    def delete_employer(self, employer):
        self.session.delete(employer)
        self.session.commit()
        return employer
