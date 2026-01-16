from sqlalchemy import desc
from app.models.Movimentations import movimentations
from app.Schemes.Movimentation_Schemes import MovimentationScheme
from sqlalchemy.orm import session

class MovimentationRepository:
    def __init__(self, session: session):
        self.session = session


    def create(self, movimentation_data: MovimentationScheme):
        new_movimentation = movimentations(part_number=movimentation_data.part_number,
                                          origin=movimentation_data.origin,
                                          reason=movimentation_data.reason,
                                          movimentation_type=movimentation_data.movimentation_type,
                                          employer=movimentation_data.employer,
                                          batch=movimentation_data.batch,
                                          qnty=movimentation_data.qnty,
                                          date=movimentation_data.date,
                                          destination=movimentation_data.destination,
                                          machining_batch=movimentation_data.machining_batch,
                                          assembly_batch=movimentation_data.assembly_batch
                                        )
        self.session.add(new_movimentation)
        self.session.commit()

    def get_all(self):
        return self.session.query(movimentations).all()

    def get_by_id(self, movimentation_id: int):
        return self.session.query(movimentations).filter(movimentations.ID == movimentation_id).first()
    
    def get_movimentation_filtered(self, 
                                   movimentation_id: int, 
                                   part_number: str = None, 
                                   batch: str = None, 
                                   start_date = None, 
                                   end_date = None,
                                   date: str = None, 
                                   employer_id: int = None,
                                     movimentation_type: str = None, 
                                     origin: str = None,
                                     destination: str = None,
                                     machining_batch: str = None,
                                     assembly_batch: str = None):
        query = self.session.query(movimentations)
        if part_number is not None:
            query = query.filter(movimentations.part_number == part_number)
        if batch is not None:
            query = query.filter(movimentations.batch == batch)
        if start_date is not None:
            query = query.filter(movimentations.date >= start_date)
        if end_date is not None:
            query = query.filter(movimentations.date <= end_date)
        if employer_id is not None:
            query = query.filter(movimentations.employer_id == employer_id)
        if movimentation_type is not None:
            query = query.filter(movimentations.movimentation_type == movimentation_type)
        if origin is not None:
            query = query.filter(movimentations.origin == origin)
        if destination is not None:
            query = query.filter(movimentations.destination == destination)
        if machining_batch is not None:
            query = query.filter(movimentations.machining_batch == machining_batch)
        if assembly_batch is not None:
            query = query.filter(movimentations.assembly_batch == assembly_batch)
        if date is not None:
            query = query.order_by(desc(movimentations.date))
        return query.all()
    
    def get_movimentation_filtered_first(self, 
                                   movimentation_id: int = None, 
                                   part_number: str = None, 
                                   batch: str = None, 
                                   start_date = None, 
                                   end_date = None,
                                   date: str = None, 
                                   employer_id: int = None,
                                     movimentation_type: str = None, 
                                     origin: str = None,
                                     destination: str = None,
                                     machining_batch: str = None,
                                     assembly_batch: str = None):
        query = self.session.query(movimentations)
        if part_number is not None:
            query = query.filter(movimentations.part_number == part_number)
        if batch is not None:
            query = query.filter(movimentations.batch == batch)
        if start_date is not None:
            query = query.filter(movimentations.date >= start_date)
        if end_date is not None:
            query = query.filter(movimentations.date <= end_date)
        if employer_id is not None:
            query = query.filter(movimentations.employer_id == employer_id)
        if movimentation_type is not None:
            query = query.filter(movimentations.movimentation_type == movimentation_type)
        if origin is not None:
            query = query.filter(movimentations.origin == origin)
        if destination is not None:
            query = query.filter(movimentations.destination == destination)
        if machining_batch is not None:
            query = query.filter(movimentations.machining_batch == machining_batch)
        if assembly_batch is not None:
            query = query.filter(movimentations.assembly_batch == assembly_batch)
        if date is not None:
            query = query.order_by(desc(movimentations.date))
        return query.first()
    

    def delete(self, movimentation_id: int):
        movimentation = self.session.query(movimentations).filter(movimentations.ID == movimentation_id).first()
        if movimentation:
            self.session.delete(movimentation)
            self.session.commit()

    def update(self, movimentation):
        self.session.commit()
        self.session.refresh(movimentation)
        return movimentation