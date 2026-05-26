from app.core import user_service
from app.presentation.schemas import UserShow
from app.infrastructure.database import get_db

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException


router_genereal = APIRouter()

@router_genereal.get('/me', response_model=UserShow)
def endpoint_check_me(current_user : dict = Depends(user_service.get_current_user), db: Session = Depends(get_db) ):
    
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token!")
    user = user_service.get_user_by_id(current_user['user_id'],db)
    return user
    

