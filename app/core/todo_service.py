from app.infrastructure.repositories import user_repository
from fastapi import Depends,HTTPException, status
from app.infrastructure.repositories import todo_repository

# ===========================================================================
def create_todo(new_todo, current_user_id, db):
    return todo_repository.create_todo_db(new_todo, current_user_id, db)
# ===========================================================================
def hard_delete_todo(todo_id, current_user, db):
    todo = todo_repository.get_todo_by_id_db(todo_id,db,current_user)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if current_user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Not allowed to delete todos")

    return todo_repository.hard_delete_todo_db(todo , db)
#------------------------------------------------------------
def soft_delete_todo(todo_id, current_user, db):
    todo = todo_repository.get_todo_by_id_db(todo_id,db, current_user)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    if (todo.user_id != current_user['user_id']) and (current_user['role'] != 'admin'):
        raise HTTPException(status_code=403, detail="Not allowed to delete this todo")

    return todo_repository.soft_delete_todo_db(todo , db)
# ===========================================================================
def get_todo_by_id(todo_id, current_user, db):
    todo = todo_repository.get_todo_by_id_db(todo_id,db,current_user)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if (todo.user_id != current_user['user_id']) and (current_user['role'] != 'admin'):
        raise HTTPException(status_code=403, detail="Not allowed to see this todo")
    
    return todo
# ===========================================================================
def get_all_todos(current_user : int, db, user_id:int = None, limit = 10, offset = 0):
    
    if user_id is not None:
        if user_repository.get_user_by_id_db(user_id , db):
            return todo_repository.get_all_todos_db(current_user,db,user_id= user_id, limit= limit, offset=offset)
        else:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User not found')
        
        
    if user_repository.get_user_by_id_db(current_user['user_id'],db):
        return todo_repository.get_all_todos_db(current_user,db,user_id= user_id, limit= limit, offset=offset)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User not found')
        
# ===========================================================================
def update_todo(todo_id, new_todo, current_user, db):
    old_todo = todo_repository.get_todo_by_id_db(todo_id,db,current_user)
    if old_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    if (old_todo.user_id != current_user['user_id']) and (current_user['role'] != 'admin'):
        raise HTTPException(status_code=403, detail="Not allowed to update this todo")
    
    return todo_repository.update_todo_db(old_todo, new_todo,current_user , db)
# ===========================================================================
def get_all_todos_with_username(current_user:int, db, limit = 10, offset = 0):
    if user_repository.get_user_by_id_db(current_user,db):
        return todo_repository.get_all_todos_with_username_db(current_user, db, limit= limit, offset=offset)
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='User not found')
    
    






