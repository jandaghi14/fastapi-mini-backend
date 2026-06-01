from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
load_dotenv()


# ===================================================
pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# ===================================================


# ===================================================
ALGORITHM = 'HS256'
SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRE_ACCESS_TIME = 30


def create_access_token(username, id, role, delta_expire: timedelta | None = None):
    if not SECRET_KEY:
        raise Exception('Secret key is being missed')

    payload = {
        'sub': username,
        'user_id': id,
        'role': role.value,
        'exp': datetime.now(timezone.utc) + (delta_expire if delta_expire else timedelta(minutes=EXPIRE_ACCESS_TIME))
    }
    try:
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise JWTError(f"Failure in creating token: {e}")


def decode_token_access(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
