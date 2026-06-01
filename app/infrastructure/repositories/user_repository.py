from sqlalchemy.orm import Session
from app.infrastructure.models import User


def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id_db(user_id, db: Session):
    return db.query(User).filter(User.id == user_id).first()


def create_user(new_user, hashed_password: str, db: Session):
    try:
        user = User(
            username=new_user.username,
            password_hash=hashed_password,
            role=new_user.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise Exception(f"Problem in creating user in database : {e}!")


def delete_user_db(user: User, db: Session):
    db.delete(user)
    db.commit()
    return True
