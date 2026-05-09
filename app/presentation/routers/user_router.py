from fastapi import APIRouter
from app.presentation import schemas
from app.core import user_service
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db


router = APIRouter()

@router.post('/register', response_model=schemas.UserShow)
def endpoint_register_user(new_user:schemas.UserCreate,db:Session = Depends(get_db)):
    result = user_service.register_user(new_user ,db)
    if result:
        return result
    raise HTTPException(status_code=409, detail="User already exists")


from fastapi.security import OAuth2PasswordRequestForm
@router.post('/login')
def login_user(data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    result =  user_service.login_user(data , db)
    if result is None:
        raise HTTPException(status_code=401, detail="Either Username or Password is wrong !")
    return result



