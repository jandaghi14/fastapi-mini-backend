
from app.infrastructure.repositories import user_repository
from app.core import authentication
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from app.presentation import schemas
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db



def register_user(new_user: schemas.UserCreate, db ):
    user = user_repository.get_user_by_username(new_user.username , db)
    if user is None:
        hashed_password = authentication.hash_password(new_user.password)
        new_user = user_repository.create_user(new_user, hashed_password, db)
        return new_user
    return None


def login_user(data, db):
    user = user_repository.get_user_by_username(data.username,db)
    if user is None:
        return None
    if authentication.verify_password(data.password , user.password_hash):
        token = authentication.create_access_token(user.username, user.id, user.role)
        return {
            "access_token" : token,
            "token_type" : "Bearer",
            "user_id" : user.id
        }
    return None


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')
from jose import JWTError
def get_current_user(token : str = Depends(oauth_scheme)):
    from fastapi import HTTPException
    try:
        decoded = authentication.decode_token_access(token)
        if decoded:
            return {'username' : decoded.get('sub'),
                    'user_id' : decoded.get('user_id'),
                    'role': decoded.get('role')}
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")

def delete_user(user_id, current_user , db):
    user =  user_repository.get_user_by_id_db(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role.value == 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="!!!Admin users cannot be deleted!!!")
    
    if user_repository.delete_user_db(user,db):
        return {'message' : f'User {user.username} with ID {user_id} deleted successfully! '}

def get_user_by_id(user_id:int, db):
    user = user_repository.get_user_by_id_db(user_id , db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "User Not found!")
    return user

