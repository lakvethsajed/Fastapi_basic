from fastapi import APIRouter, Depends, HTTPException,status
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags = ['Authetication']
)

@router.post("/login")
async def login_auth(user_details : OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db),response_model = schemas.Token_valid):
    user = db.query(models.User).filter(models.User.username == user_details.username).first()
    if user is None:
     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Ivalid credentials" )

    if not utils.verify(user_details.password, user.password):
     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Ivalid credentials" )

    access_token = oauth2.create_token(data = {"user_id": user.id})
    return {"access_token" : access_token, "token_type" : "bearer" }
      

