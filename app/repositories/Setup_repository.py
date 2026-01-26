from app.models.Setup import Setup
from app.domain.Entitys.Setup_entitys import SetupEntity
class SetupRepository:
    def __init__(self, session):
        self.session = session


    

    def create_setup(self, entity: SetupEntity ):
        new_setup = Setup(Machine=entity.machine,
                          Part_number=entity.part_number,
                          Date=entity.date,
                          Setup_time_minutes=None,
                          Check_list=None,
                          Status="PENDING",
                          Notes=entity.Notes
                          )
        
        self.session.add(new_setup)
        self.session.commit()
        return new_setup
    
    def get_all_setups(self):
        return self.session.query(Setup).all()
    
    def get_setup_filtered(self, 
                           machine: str = None,
                           part_number: str = None,
                           date: str = None,
                           emp_id: str = None,
                           status: str = None):
        
        query = self.session.query(Setup)
        
        if machine:
            query = query.filter(Setup.Machine == machine)
        if part_number:
            query = query.filter(Setup.Part_number == part_number)
        if date:
            query = query.filter(Setup.Date == date)
        if emp_id:
            query = query.filter(Setup.Emp_id == emp_id)
        if status:
            query = query.filter(Setup.Status == status)
        
        return query.all()

