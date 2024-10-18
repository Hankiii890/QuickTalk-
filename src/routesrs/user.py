from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Логика аутентификации"""
    pass


@router.post("/register")
async def register():
    """Логика регистрации"""
    pass
