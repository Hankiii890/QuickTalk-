from fastapi import FastAPI
from routesrs.user import router

app = FastAPI()

app.include_router(router)
