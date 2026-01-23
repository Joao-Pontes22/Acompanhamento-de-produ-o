# FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemes
from app.Schemas.Components_Schemas import ComponentsSchema, UpdateComponentsInfoSchema
from app.Schemas.Responses.Response_Components import ResponseComponents
from app.Schemas.Queries.components_query_params import ComponentsParameters
#Repository
from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Suppliers_repository import SuppliersRepository

from app.Services.Components_Service import ComponentsService

from app.domain.Exceptions import AlreadyExist, NotFoundException
Components_Router = APIRouter(prefix="/Components", tags=["Components Operations"])


@Components_Router.post("/create_component")
async def add_component(body: ComponentsSchema,
                        session: Session = Depends(Init_Session)
                        ):
    
    repo = ComponentsRepository(session=session)
    supllier_repo = SuppliersRepository(session=session)
    service = ComponentsService(components_repo=repo)

    try:
        new_component = service.create_components(schema=body, 
                                                  supplier_repo=supllier_repo
                                                  )
        
        return {"message": "Component created successful",
            "Component": new_component.part_number}
    
    except AlreadyExist as e:
        raise HTTPException(status_code=409, detail=str(e))
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@Components_Router.get("/get_all_components", 
                       response_model=list[ResponseComponents]
                       )
async def get_components(session:Session=Depends(Init_Session)):

    repo = ComponentsRepository(session=session)
    service = ComponentsService(components_repo=repo)

    try:
        components = service.get_all_component()
        return components
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Components_Router.get("/get_components_filtered", response_model=list[ResponseComponents])
async def get_components_filtered(query_params: ComponentsParameters = Depends(),
                                  session:Session=Depends(Init_Session)):
    
    repo = ComponentsRepository(session=session)
    service = ComponentsService(components_repo=repo)
    
    try:
        components = service.get_component_filtred(query_params=query_params)
        
        return components
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Components_Router.patch("/update_component_info/{part_number}")
async def update_component(body:UpdateComponentsInfoSchema,
                           query_params:ComponentsParameters = Depends(),  
                           session:Session=Depends(Init_Session)):
                           
   
    repo = ComponentsRepository(session=session)
    supllier_repo = SuppliersRepository(session=session)
    service = ComponentsService(components_repo=repo)
    
    try:
        updated_component = service.update_component_info(query_params=query_params, 
                                                          schema=body, 
                                                          supplier_repo=supllier_repo)
        return {"message": "Component updated successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@Components_Router.delete("/delete_component/{part_number}")
async def delete_component(part_number:str, 
                           session:Session = Depends(Init_Session)
                           ):
    repo = ComponentsRepository(session=session)
    service = ComponentsService(components_repo=repo)
    try:
        deleted_component = service.delete_component(part_number=part_number)
        return {"message": "Component deleted successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

