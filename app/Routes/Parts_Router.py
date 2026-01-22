#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemas and response
from app.Schemas.Parts_Schemas import PartsSchema, UpdatePartsInfoSchema
from  app.Schemas.Responses.Response_Parts import ResponseParts
#Repository
from app.repositories.Parts_repository import PartsRepository
from app.repositories.Clients_repository import ClientsRepository
#Service
from app.Services.Parts_Service import Parts_Services
#Exception
from app.domain.Exceptions import NotFoundException, AlreadyExist

Part_Router = APIRouter(prefix="/Parts", tags=["Parts Operations"])
                

@Part_Router.post("/add_parts")
async def add_part(schemes: PartsSchema, 
                   session: Session = Depends(Init_Session)
                   ):

    repo = PartsRepository(session=session)
    service = Parts_Services(parts_repo=repo)
    clients_repo = ClientsRepository(session=session)

    try:
        new_part = service.create_part(scheme=schemes,clients_repo=clients_repo)

        return {"message": "Part created successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExist as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@Part_Router.get("/get_parts", 
                 response_model=list[ResponseParts]
                 )
async def get_part(session: Session = Depends(Init_Session)):

    repo = PartsRepository(session=session)
    service = Parts_Services(parts_repo=repo)
    try:

        return service.get_all_parts()
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Part_Router.patch("/update_part/{part_number}")
async def update_part(part_number: str, 
                      scheme: UpdatePartsInfoSchema, 
                      session: Session = Depends(Init_Session)
                      ):
    repo = PartsRepository(session=session)
    clients_repo = ClientsRepository(session=session)
    service = Parts_Services(parts_repo=repo)

    try:
        Updated_part = service.update_part_info(part_number=part_number, scheme=scheme, clients_repo=clients_repo)
        
        return {"message": "Parts updated successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Part_Router.get("/Get_parts_filtered", 
                 response_model=list[ResponseParts]
                 )

async def get_filtered_parts(id:int = None, 
                             part_number:str = None, 
                             description:str = None, 
                             client:str = None, 
                             session:Session = Depends(Init_Session)
                             ):
    repo = PartsRepository(session=session)
    service = Parts_Services(parts_repo=repo)
    try:
        filtered_parts = service.get_filtred_parts(id=id, 
                                                    part_number=part_number, 
                                                    description=description, 
                                                    client=client
                                                    )
        return filtered_parts
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Part_Router.delete("/Delete_part/{part_number}")
async def delete_part(part_number: str, 
                      session:Session = Depends(Init_Session)
                      ):
    
    repo = PartsRepository(session=session)
    service = Parts_Services(parts_repo=repo)
    try:
        deleted = service.delete_part(part_number=part_number)

        return {"message": "Part deleteded successful"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

