from fastapi import FastAPI


app = FastAPI()
app.get("/Root")
async def Root():
    return "Rota principal"


from app.Routes.Employer_Router import Employer_Router
from app.Routes.Sector_Routes import Sector_Router
from app.Routes.Login_Router import Login_Router
from app.Routes.Supplier_Router import Supplier_Router
from app.Routes.Clients_Router import Client_Router
from app.Routes.Stock_Router import Stock_Router
from app.Routes.Machine_Router import Machine_Router
from app.Routes.Components_Router import Components_Router
app.include_router(Employer_Router)
app.include_router(Sector_Router)
app.include_router(Login_Router)
app.include_router(Supplier_Router)
app.include_router(Client_Router)
app.include_router(Stock_Router)
app.include_router(Machine_Router)
app.include_router(Components_Router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)