from sqlalchemy.orm import Session, joinedload
from app.infrastructure.models import Todo
from sqlalchemy.sql import func
from app.infrastructure.repositories.user_repository import get_user_by_id_db
from app.infrastructure.repositories import user_repository


def create_todo_db(new_todo, current_user_id, db:Session):
    try:
        todo = Todo(
            title = new_todo.title,
            description = new_todo.description,
            priority = new_todo.priority,
            due_date = new_todo.due_date,
            user_id = current_user_id
            
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        raise e
    

def get_todo_by_id_db(todo_id,db:Session, current_user = None):
    
    if current_user['role'] == 'admin':
        return db.query(Todo).filter(Todo.id == todo_id).first()

    return db.query(Todo).filter(Todo.id == todo_id, Todo.is_deleted == False).first()
    
    
def hard_delete_todo_db(todo:Todo, db:Session):

    db.delete(todo)
    db.commit()
    return True

def soft_delete_todo_db(todo:Todo, db:Session):
    todo.is_deleted = True
    db.commit()
    db.refresh(todo)
    return True

def get_all_todos_db(current_user, db:Session, limit = 10, offset= 0, user_id : int = None):
    if user_id:
        if user_repository.get_user_by_id_db(user_id,db):
            return db.query(Todo).filter(Todo.user_id == user_id).limit(limit).offset(offset).all()
        else:
            return None
        
    if current_user['role'] != 'admin':
        return db.query(Todo).filter(Todo.user_id == current_user["user_id"], Todo.is_deleted == False).limit(limit).offset(offset).all()
    return db.query(Todo).filter(Todo.user_id == current_user["user_id"]).limit(limit).offset(offset).all()

def update_todo_db(old_todo, new_todo, current_user,db:Session): 
    if current_user['role'] == 'admin':
        if hasattr(new_todo, 'is_deleted') and new_todo.is_deleted is not None:
            old_todo.is_deleted = new_todo.is_deleted
        if hasattr(new_todo, 'user_id') and new_todo.user_id is not None:
            old_todo.user_id = new_todo.user_id
    
    
    if new_todo.title is not None:
        old_todo.title = new_todo.title
    if new_todo.description is not None:
        old_todo.description = new_todo.description
    if new_todo.status is not None:
        old_todo.status = new_todo.status
    if new_todo.priority is not None:
        old_todo.priority = new_todo.priority
    if new_todo.due_date is not None:
        old_todo.due_date = new_todo.due_date
        
        
    old_todo.updated_at = func.now()
    
    db.commit()
    db.refresh(old_todo)
    return old_todo



def get_all_todos_with_username_db(current_user:int, db:Session, limit = 10, offset = 0):
    return db.query(Todo).options(joinedload(Todo.owner)).filter(Todo.user_id == current_user).all()
