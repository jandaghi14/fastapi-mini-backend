from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.presentation.schemas import TodoCreate, TodoShow, TodoUpdate,TodoShowUpdate
from app.core.user_service import get_current_user
from app.core import todo_service
from app.core.security import require_role

todo_router = APIRouter(prefix="/todos", tags=["Todos"])


@todo_router.post('/create_todo', response_model= TodoShow)
def endpoint_create_todo(new_todo : TodoCreate ,
                         current_user : dict = Depends(get_current_user),
                         db : Session= Depends(get_db)):
    
    return todo_service.create_todo(new_todo ,current_user['user_id'], db)
# ===============================================================================================================================

#-------------------------------------------------------------------------- 
@todo_router.delete('/delete_todo/{todo_id}',response_model= dict)
def endpoint_soft_delete_todo(todo_id : int , 
                         current_user : dict = Depends(get_current_user),
                         db : Session= Depends(get_db)):
    
    todo_service.soft_delete_todo(todo_id ,current_user, db)
   
    return {"message" : f"Todo by ID {todo_id} soft deleted successfully!"}
# ===============================================================================================================================
@todo_router.get('/get_todo_by_id/{todo_id}', response_model= TodoShow)
def endpoint_get_todo_by_id(todo_id : int , 
                         current_user : dict = Depends(get_current_user),
                         db : Session= Depends(get_db)):
    
    return todo_service.get_todo_by_id(todo_id ,current_user, db)
# ===============================================================================================================================
@todo_router.get('/get_all_todos', response_model= list[TodoShow])
def endpoint_get_all_todos(limit : int =10,
                           offset : int = 0,
                           current_user : dict = Depends(get_current_user),
                           db : Session= Depends(get_db),
                           ):
    
    return todo_service.get_all_todos(current_user, db, limit =limit, offset = offset)
# ===============================================================================================================================
@todo_router.put('/update_todo/{todo_id}',response_model=TodoShowUpdate)
def endpoint_update_todo(todo_id:int,
                         new_todo : TodoUpdate,
                         current_user : dict = Depends(get_current_user),
                         db : Session= Depends(get_db)
                         ):
    return todo_service.update_todo(todo_id, new_todo, current_user, db)






























