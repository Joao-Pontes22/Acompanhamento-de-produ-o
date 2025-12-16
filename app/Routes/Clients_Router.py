from fastapi import APIRouter, Depends
from app.core.Dependecies import Init_Session
from sqlalchemy.orm import Session
from app.Schemes.Clients_Schemes import Clients_Scheme, Clients_Update_Scheme
from app.repositories.Clients_repositorie import Clients_repositorie
from app.Services.Client_Services import Clients_Services
Client_Router = APIRouter(prefix="/Clients", tags=["Clients Operations"])

@Client_Router.post("/add_client")
async def add_client(scheme: Clients_Scheme, session: Session = Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    new_client = service.service_create_clients(scheme=scheme)
    return{"message": "Client created successfuly",
           "Client": new_client.name}

@Client_Router.get("/Get_all_clients")
async def get_all_clients(session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    clients = service.service_get_all_clients()
    return clients

@Client_Router.get("/Get_by_ID{id}")
async def get_by_id(id:int, session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service= Clients_Services(repo=repo)
    client = service.service_get_by_id(ID=id)
    return client

@Client_Router.patch("/update_client_by_id{id}")
async def update_by_id(id:int, scheme:Clients_Update_Scheme, session:Session = Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    new_client = service.update_client_info(ID=id, scheme=scheme)
    return new_client

@Client_Router.delete("/Delete_client")
async def delete_client(id:int, session:Session=Depends(Init_Session)):
    repo = Clients_repositorie(session=session)
    service = Clients_Services(repo=repo)
    client = service.service_delete_client(ID=id)
    return {"message": "Client deleted successfuly",
            "Client":client}