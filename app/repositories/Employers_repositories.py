from app.models.Employers import Employers


class employersRepo:
    def __init__(self,session):
        self.session = session

    def repo_get_all_employers(self):
        employers = self.session.query(Employers).all()
        return employers
    
    def repo_find_by_id(self, id:int):
        self.id = id
        return self.session.query(Employers).filter(Employers.ID == id).first()
    
    def repo_find_by_emp_id(self, emp_id):
        employer = self.session.query(Employers).filter(Employers.emp_id == emp_id).first()
        return employer
    
    def repo_create_employer(self, name, sector, password, emp_id):
        new_employer = Employers(name=name,
                                 password=password,
                                 sector_name=sector,
                                 emp_id=emp_id)
        self.session.add(new_employer)
        self.session.commit()
        return new_employer
    
    def repo_delete_employer(self, employer):
        self.session.delete(employer)
        self.session.commit()
        return employer
