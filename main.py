from fastapi import FastAPI, Request

app = FastAPI()
@app.get("/Root")
async def Root():
    return "Rota principal"


from app.Routes.Employer_Router import Employer_Router
from app.Routes.Sector_Router import Sector_Router
from app.Routes.Login_Router import Login_Router
from app.Routes.Supplier_Router import Supplier_Router
from app.Routes.Clients_Router import Client_Router
from app.Routes.Stock_Router import Stock_Router
from app.Routes.Machine_Router import Machine_Router
from app.Routes.Components_Router import Components_Router
from app.Routes.Parts_Router import Part_Router
from app.Routes.Stock_Router import Stock_Router
from app.Routes.Movimentation_Router import Movimentaion_Router
from app.Routes.Relation_Router import PartsxComponents_Router
from app.domain.Exceptions import AlreadyExist
from fastapi.responses import JSONResponse

@app.exception_handler(AlreadyExist)
async def already_exist_handler(request: Request, exc: AlreadyExist):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

app.include_router(Sector_Router)
app.include_router(Employer_Router)
app.include_router(Login_Router)
app.include_router(Supplier_Router)
app.include_router(Client_Router)
app.include_router(Components_Router)
app.include_router(Part_Router)
app.include_router(Stock_Router)
app.include_router(Movimentaion_Router)
app.include_router(Machine_Router)
app.include_router(PartsxComponents_Router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)