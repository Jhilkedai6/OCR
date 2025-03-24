from fastapi import FastAPI
from Router import crud, auth, admin
import model
from database import Engine
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(bind=Engine)

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="q90ZxmK4rtjfu!394KDkfj29Kjd9x@kdjfs093klsdf")


app.include_router(crud.router)
app.include_router(auth.router)
app.include_router(admin.router)


