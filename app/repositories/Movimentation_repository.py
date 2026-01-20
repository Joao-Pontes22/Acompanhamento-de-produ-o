from sqlalchemy import desc
from app.models.Movimentations import movimentations
from sqlalchemy.orm import session

class MovimentationRepository:
    def __init__(self, session: session):
        self.session = session


    def create_movimentation(self, 
               part_number: str,
               sector_origin: str,
               reason: str,
               movimentation_type: str,
               emp_id: str,
               batch:str,
               qnty:int,
               date,
               sector_destination: str,
               machining_batch: str,
               assembly_batch: str
               ):
        new_movimentation = movimentations(part_number=part_number,
                                           origin=sector_origin,
                                           reason=reason,
                                           movimentation_type=movimentation_type,
                                           employer=emp_id,
                                           batch=batch,
                                           qnty=qnty,
                                           date=date,
                                           destination=sector_destination,
                                           machining_batch=machining_batch,
                                           assembly_batch=assembly_batch
                                           )
        self.session.add(new_movimentation)
        self.session.commit()

    def get_all(self):
        return self.session.query(movimentations).all()

    def get_by_id(self, movimentation_id: int):
        return self.session.query(movimentations).filter(movimentations.ID == movimentation_id).first()
    
    def get_movimentation_filtered(self, 
                                   movimentation_id: int, 
                                   part_number: str, 
                                   batch: str, 
                                   start_date, 
                                   end_date,
                                   emp_id: int,
                                   movimentation_type: str, 
                                   origin: str,
                                   destination: str,
                                   machining_batch: str,
                                   assembly_batch: str
                                   ):
        query = self.session.query(movimentations)
        if part_number:
            query = query.filter(movimentations.part_number == part_number)
        if batch:
            query = query.filter(movimentations.batch == batch)
        if start_date:
            query = query.filter(movimentations.date >= start_date)
        if end_date :
            query = query.filter(movimentations.date <= end_date)
        if emp_id:
            query = query.filter(movimentations.employer == emp_id)
        if movimentation_type:
            query = query.filter(movimentations.movimentation_type == movimentation_type)
        if origin:
            query = query.filter(movimentations.origin == origin)
        if destination:
            query = query.filter(movimentations.destination == destination)
        if machining_batch:
            query = query.filter(movimentations.machining_batch == machining_batch)
        if assembly_batch:
            query = query.filter(movimentations.assembly_batch == assembly_batch)
        if movimentation_id:
            query = query.order_by(desc(movimentations.ID))
        return query.all()
    
    def get_movimentation_filtered_first(self, 
                                         movimentation_id: int, 
                                         part_number: str, 
                                         batch: str, 
                                         start_date, 
                                         end_date,
                                         emp_id: str,
                                         movimentation_type: str, 
                                         origin: str,
                                         destination: str,
                                         machining_batch: str,
                                         assembly_batch: str
                                         ):
        query = self.session.query(movimentations).filter(movimentations.movimentation_type == "CREATE")
        if part_number:
            query = query.filter(movimentations.part_number == part_number)
        if batch:
            query = query.filter(movimentations.batch == batch)
        if start_date:
            query = query.filter(movimentations.date >= start_date)
        if end_date:
            query = query.filter(movimentations.date <= end_date)
        if emp_id:
            query = query.filter(movimentations.employer == emp_id)
        if movimentation_type:
            query = query.filter(movimentations.movimentation_type == movimentation_type)
        if origin:
            query = query.filter(movimentations.origin == origin)
        if destination:
            query = query.filter(movimentations.destination == destination)
        if machining_batch:
            query = query.filter(movimentations.machining_batch == machining_batch)
        if assembly_batch:
            query = query.filter(movimentations.assembly_batch == assembly_batch)
        if movimentation_id:
            query = query.order_by(desc(movimentations.ID))
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