
from app.infrastructure.repositories import user_repository
from app.core import authentication
from app.core.logger import logger
from app.presentation import schemas
from app.infrastructure.database import get_db
#============================
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session



def register_user(new_user: schemas.UserCreate, db ):
    user = user_repository.get_user_by_username(new_user.username , db)
    if user is None:
        hashed_password = authentication.hash_password(new_user.password)
        new_user = user_repository.create_user(new_user, hashed_password, db)
        logger.info(f'New user with username : {new_user.username} is created!')
        return new_user

    logger.warning(f'An unsuccessful try to register already-exist user with username : {new_user.username}')
    return None


def login_user(data, db):
    user = user_repository.get_user_by_username(data.username,db)
    if user is None:
        logger.warning(f'An unsuccessful try to log in with unavailable username : {data.username}')
        return None
    if authentication.verify_password(data.password , user.password_hash):
        token = authentication.create_access_token(user.username, user.id, user.role)
        logger.info(f'Token created successfully with username : {data.username}')
        return {
            "access_token" : token,
            "token_type" : "Bearer",
            "user_id" : user.id
        }
    logger.warning(f'User with username :{data.username} entered a wrong password')
    return None


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')
from jose import JWTError
def get_current_user(token : str = Depends(oauth_scheme)):
    from fastapi import HTTPException
    try:
        decoded = authentication.decode_token_access(token)
        if decoded:
            logger.info(f"The provided username:'{decoded.get('sub')}' and password were decoded successfully")
            return {'username' : decoded.get('sub'),
                    'user_id' : decoded.get('user_id'),
                    'role': decoded.get('role')}
            
        logger.warning(f"The username:'{decoded.get('sub')}' and password produced Invalid Token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except JWTError:
        logger.warning("Authentication failed — invalid or expired token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")

def delete_user(user_id, current_user , db):
    user =  user_repository.get_user_by_id_db(user_id, db)
    if user is None:
        logger.warning(f'An unsuccessful try to delete with unavailable username in database')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role.value == 'admin':
        logger.warning(f'An unsuccessful try to delete Admin users')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="!!!Admin users cannot be deleted!!!")
    
    if user_repository.delete_user_db(user,db):
        logger.info(f"User with username '{user.username}' soft deleted successfully")
        return {'message' : f'User {user.username} with ID {user_id} deleted successfully! '}

def get_user_by_id(user_id:int, db):
    user = user_repository.get_user_by_id_db(user_id , db)
    logger.info(f"Hitting the database to get_user_by_id")
    if user is None:
        logger.warning(f"User with with user_id {user_id} could not be found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= "User Not found!")
    logger.info(f"User with user_id '{user_id}' with username:'{user.username}' returned successfully")
    return user

