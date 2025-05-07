from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app import models, oauth2
from app.database import get_db
from app.schemas import Token
from app.utils import verify

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # OAuth2PasswordRequestForm - This will return these two variables:
    # {
    #     "username": "demouser",
    #     "password": "pass123"
    # }

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # Create a token and return the token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token" : access_token, "token_type": "bearer"}