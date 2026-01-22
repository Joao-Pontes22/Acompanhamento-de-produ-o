
# FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#Session
from sqlalchemy.orm import Session
#Schemes and Responses
from app.Schemas.Clients_Schemas import ClientsSchema, UpdateClientsInfoSchema
from app.Schemas.Responses.Response_Clients import ResponseClients
#Repositories
from app.repositories.Clients_repository import ClientsRepository
from app.repositories.Sectors_repository import SectorsRepository
#Services
from app.Services.Client_Service import ClientsService
#Exceptions
from app.domain.Exceptions import AlreadyExist, InvalidNameException, NotFoundException



Client_Router = APIRouter(prefix="/Clients", tags=["Clients Operations"])


@Client_Router.post("/create_client")
async def create_client(scheme: ClientsSchema, session: Session = Depends(Init_Session)):
    
    repo = ClientsRepository(session=session)
    service = ClientsService(repo=repo)

    try:
        new_client = service.create_client(schema=scheme)

        return{"message": "Client created successfuly",
                "Client": new_client.name}
    
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))



@Client_Router.get("/get_all_clients", response_model=list[ResponseClients])
async def get_all_clients(session:Session=Depends(Init_Session)):

    repo = ClientsRepository(session=session)
    service = ClientsService(repo=repo)

    try:
        clients = service.get_all_clients()
        return clients
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@Client_Router.get("/get_by_name/{client}", response_model=ResponseClients)
async def get_by_name(client:str, 
                      session:Session=Depends(Init_Session)):

    repo = ClientsRepository(session=session)
    service= ClientsService(repo=repo)

    try:
        client = service.get_by_name(name=client)
        return client
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@Client_Router.patch("/update_client_by_name/{client}", response_model=ResponseClients)
async def update_by_name(client:str, 
                         scheme:UpdateClientsInfoSchema, 
                         session:Session = Depends(Init_Session)):
   
    repo = ClientsRepository(session=session)
    service = ClientsService(repo=repo)

    try:

        new_client = service.update_client_info(name=client, schema=scheme)

        return new_client
    
    except InvalidNameException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@Client_Router.delete("/delete_client/{client}")
async def delete_client(client:str, session:Session=Depends(Init_Session)):

    repo = ClientsRepository(session=session)
    service = ClientsService(repo=repo)

    try:

        client = service.delete_client(name=client)

        return {"message": "Client deleted successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
