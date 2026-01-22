# FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Dependecies
from app.core.Dependecies import Init_Session
#SQLAlchemy
from sqlalchemy.orm import Session
#Schemes and response
from app.Schemas.Components_Schemas import ComponentsSchema, UpdateComponentsInfoSchema
from app.Schemas.Responses.Response_Components import ResponseComponents
#Repository
from app.repositories.Components_repository import ComponentsRepository
from app.repositories.Suppliers_repository import SuppliersRepository

from app.Services.Components_Service import ComponentsService

from app.domain.Exceptions import AlreadyExist, NotFoundException
Components_Router = APIRouter(prefix="/Components", tags=["Components Operations"])


@Components_Router.post("/add_component")
async def add_component(schema: ComponentsSchema,
                        session: Session = Depends(Init_Session)
                        ):
    
    repo = ComponentsRepository(session=session)
    supllier_repo = SuppliersRepository(session=session)
    service = ComponentsService(components_repo=repo)

    try:
        new_component = service.create_components(schema=schema, 
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
async def get_components_filtered(id:int = None,
                                  part_number:str = None, 
                                  description:str = None, 
                                  supplier:str = None, 
                                  component_type:str = None, 
                                  session:Session=Depends(Init_Session)):
    
    repo = ComponentsRepository(session=session)
    service = ComponentsService(components_repo=repo)
    
    try:
        components = service.get_component_filtred(id=id,part_number=part_number, description=description, supplier=supplier, component_type=component_type)
        
        return components
    
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))


@Components_Router.patch("/update_component_info/{part_number}", 
                         response_model=ResponseComponents
                         )
async def update_component(part_number:str, 
                           schema:UpdateComponentsInfoSchema, 
                           session:Session=Depends(Init_Session)):
   
    repo = ComponentsRepository(session=session)
    supllier_repo = SuppliersRepository(session=session)
    service = ComponentsService(components_repo=repo)
    
    try:
        updated_component = service.update_component_info(part_number=part_number.upper(), 
                                                          schema=schema, 
                                                          supplier_repo=supllier_repo)
        return {"message": "Component updated successfuly"}
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@Components_Router.delete("/Delete_component/{part_number}")
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

