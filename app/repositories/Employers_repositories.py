from app.models.Models import Employers


class employersRepo:
    def __init__(self,session):
        self.session = session

    def repo_get_all_employers(self):
        employers = self.session.query(Employers).all()
        return employers
    
    def repo_find_by_id(self,id):
        self.id = id
        return self.session.query(Employers).filter(Employers.ID == id).first()
    
    def repo_find_by_name(self,name):
        self.name = name
        employer = self.session.query(Employers).filter(Employers.name == name).first()
        return employer
    
    def repo_create_employer(self, name, sector_id, password ):
        self.name = name
        self.sector_id = sector_id
        self.password = password
        new_employer = Employers(name=self.name,
                                 password=self.password,
                                 sector=self.sector_id)
        self.session.add(new_employer)
        self.session.commit()
        return new_employer
    
    def repo_delete_employer(self, employer):
        self.session.delete(employer)
        self.session.commit()
        return employer
