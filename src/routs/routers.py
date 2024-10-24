from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from routs.models import UserCreated, TokenData
from database import get_db
from models.us_me import Users

router = APIRouter()

SECRET_KEY = "001789a17b33865b6c2be5f50f36d7c1a34bc6096bbc843cb97e960446310ab4"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # Процедуры хеширования и генерации пароля
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@router.post("/register")
async def register_user(user: UserCreated, db: Session = Depends(get_db)):
    # Проверка на существование юзера
    existing_user = db.query(Users).filter(Users.name == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    hashed_password = pwd_context.hash(user.password)

    # Create new user
    new_user = Users(name=user.username, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"Message": "Пользователь успешно зарегистрирован!"}
