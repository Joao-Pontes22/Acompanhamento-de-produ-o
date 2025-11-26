from fastapi import FastAPI


app = FastAPI()
app.get("/Root")
async def Root():
    return "Rota principal"


from Routes.Auth_Router import Auth_Router
from Routes.Sector_Routes import Sector_Router
from Routes.Login_Router import Login_Router
from Routes.Supplier_Router import Supplier_Router
from Routes.Data_Router import Data_Router
app.include_router(Auth_Router)
app.include_router(Sector_Router)
app.include_router(Login_Router)
app.include_router(Supplier_Router)
app.include_router(Data_Router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)