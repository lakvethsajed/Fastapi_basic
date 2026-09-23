from jose import JWTError, jwt
from datetime import datetime ,timedelta ,timezone
from . import schemas
from fastapi import status,HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from . database import get_db
from sqlalchemy.orm import Session
from . import models
from .config import settings
oauth_scheme = OAuth2PasswordBearer(tokenUrl= "login")

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt


def validate_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        user_id : str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.Tokendata(id = str(user_id))
    except JWTError:
        raise credentials_exception
    return token_data

def current_user(token : str = Depends(oauth_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not verify the credentials", headers={"WWW-Authenticate": "Bearer"})
    token_data = validate_token(token , credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
def admin_user(current_user = Depends(current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "only admin can perform this operation")
    return current_user

def normal_user(current_user = Depends(current_user)):
    if current_user.role != "user":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "Admin cannot borrow or return books or see user books")
    return current_user