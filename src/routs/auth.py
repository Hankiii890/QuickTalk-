from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from routs.models import UserCreated, TokenData
from database import get_db
from models.us_me import Users
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # Процедуры хеширования и генерации пароля
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

template = Jinja2Templates(directory="templates")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создание токена"""
    to_encode = data.copy()    # Копия входящего словаря, чтобы избежать его изменения
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})   # Храним срок действия токена
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str, credentials_exceptions: HTTPException):
    """Функция для проверки и декодирования токена,
    чтобы убедиться, что он действителен и извлечь данные о юзере
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exceptions
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exceptions
    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exeptions = HTTPException(status_code=401, detail="Could not validate credentials")
    token_data = verify_token(token, credentials_exeptions)
    user = db.query(Users).filter(Users.name == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get("/")
async def home(request: Request):
    return template.TemplateResponse("index.html", {"request": request})


@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return template.TemplateResponse("chat.html", {"request": request})


@router.post("/login")
async def login(reqeust: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.name == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Неверные логин или пароль!")

    # Создание токена
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)


    # Возвращаем токен
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверка на существование юзера
    existing_user = db.query(Users).filter(Users.name == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    hashed_password = pwd_context.hash(password)

    # Создание нового пользователя
    new_user = Users(name=username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"Message": "Пользователь успешно зарегистрирован!"}


@router.get("/users")
async def get_user(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id != current_user.id).all()
    return user