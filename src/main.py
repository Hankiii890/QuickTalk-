from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from models import User

app = FastAPI()

oauth2_sheme = OAuth2PasswordBearer(tokenUrl='token')


def fake_hash_password(password: str):
    return "fakehashed" + password


class UserInDb(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        pass


def fake_decoder_token(token):
    return User(
        username=token + 'fakedecoder', email="kirill@gmail.com", fullname="Shenderuk Kirill"
    )


async def get_current_user(token: str = Depends(oauth2_sheme)):
    user = fake_decoder_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
