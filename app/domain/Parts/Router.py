#FastAPI
from fastapi import APIRouter, Depends, HTTPException
#Schema
from app.domain.Parts.Schema import PartsSchema, UpdatePartsInfoSchema
from  app.domain.Parts.Response import ResponseParts
from app.domain.Parts.Query_Params import PartsParameters
#Dependecies
from app.core.Services_dependecies import get_services
from app.core.Repositories_dependecies import get_machining_production_repos
#Exception
from app.domain.Exceptions import NotFoundException, AlreadyExist

Part_Router = APIRouter(prefix="/Parts", tags=["Parts Operations"])
                

@Part_Router.post("/add_parts")
async def add_part(body: PartsSchema, 
                   repos = Depends(get_machining_production_repos),
                   service = Depends(get_services)):

    parts_service = service["Parts"]

    try:
        new_part = parts_service.create_part(scheme=body, clients_repo=repos["clients"])

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
async def get_part(service = Depends(get_services)):

    parts_service = service["Parts"]
    try:

        return parts_service.get_all_parts()
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Part_Router.patch("/update_part/{part_number}")
async def update_part(part_number: str, 
                      body: UpdatePartsInfoSchema, 
                      repos = Depends(get_machining_production_repos),
                      service = Depends(get_services)):
    parts_service = service["Parts"]

    try:
        Updated_part = parts_service.update_part_info(part_number=part_number, scheme=body, clients_repo=repos["clients"])
        
        return {"message": "Parts updated successfuly"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@Part_Router.get("/get_parts_filtered", 
                 response_model=list[ResponseParts]
                 )

async def get_filtered_parts(query_params: PartsParameters = Depends(),
                             service = Depends(get_services)):
    parts_service = service["Parts"]
    try:
        filtered_parts = parts_service.get_filtred_parts(query_params= query_params)
        return filtered_parts
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@Part_Router.delete("/Delete_part/{part_number}")
async def delete_part(part_number: str, 
                      service = Depends(get_services)):
    
    parts_service = service["Parts"]
    try:
        deleted = parts_service.delete_part(part_number=part_number)

        return {"message": "Part deleteded successful"}
    
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

