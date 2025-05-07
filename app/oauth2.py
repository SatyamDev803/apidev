from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#SECRET_KEY
SECRET_KEY = settings.secret_key

#ALGORITHM
ALGORITHM = settings.algorithm

#EXPIRATION TIME
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp" : expire})

#     encoded_jwt =  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt


# def verify_access_token(token: str, credentials_exceptions):

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#         id: str = payload.get("user_id")

#         if id is None:
#             raise credentials_exceptions
#         token_data = TokenData(id=id)
    
#     except PyJWTError as e:
#         raise credentials_exceptions

#     return token_data


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["user_id"] = str(to_encode["user_id"])  # Ensure user_id is a string
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credentials_exceptions

        token_data = TokenData(id=str(id))  # Convert id to string
    except PyJWTError as e:
        raise credentials_exceptions

    return token_data

    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user