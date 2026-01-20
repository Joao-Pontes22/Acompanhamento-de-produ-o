
# FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#Session
from sqlalchemy.orm import Session
#Schemes and Responses
from app.Schemes.Clients_Schemes import ClientsScheme, UpdateClientsInfoScheme
from app.Schemes.Responses.Response_Clients import Response_clients_scheme
#Repositories
from app.repositories.Clients_repository import ClientsRepository
from app.repositories.Sectors_repository import SectorsRepository
#Services
from app.Services.Client_Service import Clients_Services
#Exceptions
from app.domain.Exceptions import AlreadyExist, InvalidNameException, NotFoundException



Client_Router = APIRouter(prefix="/Clients", tags=["Clients Operations"])

@Client_Router.post("/add_client")
async def add_client(scheme: ClientsScheme, session: Session = Depends(Init_Session)):
    repo = ClientsRepository(session=session)
    service = Clients_Services(repo=repo)
    try:
        new_client = service.service_create_clients(scheme=scheme)
        return{"message": "Client created successfuly",
            "Client": new_client.name}
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidNameException as e:
        raise HTTPException(status_code=400, detail=str(e))

@Client_Router.get("/Get_all_clients", response_model=list[Response_clients_scheme])
async def get_all_clients(session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    try:
        clients = service.service_get_all_clients()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return clients

@Client_Router.get("/Get_by_name/{client}", response_model=Response_clients_scheme)
async def get_by_name(client:str, session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service= Clients_Services(repo=repo)
    try:
        client = service.service_get_by_name(name=client)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return client

@Client_Router.patch("/update_client_by_name/{client}", response_model=Response_clients_scheme)
async def update_by_name(client:str, scheme:Clients_Update_Scheme, session:Session = Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    try:
        new_client = service.update_client_info(name=client, scheme=scheme)
    except InvalidNameException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return new_client

@Client_Router.delete("/Delete_client/{client}")
async def delete_client(client:str, session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    try:
        client = service.service_delete_client(name=client)
        return {"message": "Client deleted successfuly",
                "Client":client}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
