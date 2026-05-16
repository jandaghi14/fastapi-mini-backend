from fastapi import APIRouter, Depends, status, HTTPException

from app.core.security import require_role
from app.core.todo_service import hard_delete_todo
from app.core.user_service import delete_user
from app.infrastructure.database import get_db
from app.presentation.schemas import TodoShow,TodoShowUpdate, TodoShowWithOwner, TodoUpdateAdmin
from app.core.user_service import get_current_user
from app.core import todo_service

from sqlalchemy.orm import Session

router_admin = APIRouter(prefix='/admin', tags=['Admin'])

@router_admin.get('/')
def admin_panel(user = Depends(require_role('admin'))):
    return {'message': 'Welcome admin'}
# ===============================================================================================================================
@router_admin.delete('/hard_delete_todo/{todo_id}',response_model= dict)
def endpoint_hard_delete_todo(todo_id : int , 
                         current_user  = Depends(require_role('admin')),
                         db : Session= Depends(get_db)):
    
    hard_delete_todo(todo_id ,current_user, db)
   
    return {"message" : f"Todo by ID {todo_id} hard deleted successfully!"}
# ===============================================================================================================================
@router_admin.delete('/delete_user/{user_id}',response_model= dict)
def endpoint_delete_user(user_id : int , 
                         current_user  = Depends(require_role('admin')),
                         db : Session= Depends(get_db)):
    return delete_user(user_id, current_user , db)


#========================Related to other Users====================================
@router_admin.get('/get_todo_by_id/{todo_id}', response_model= TodoShow)
def endpoint_get_todo_by_id(todo_id : int ,
                            current_user : dict = Depends(require_role('admin')),
                            db : Session= Depends(get_db)):
    
    return todo_service.get_todo_by_id(todo_id ,current_user, db)
# ===============================================================================================================================
@router_admin.get('/get_all_todos/{user_id}', response_model=list[TodoShow])
def endpoint_get_all_todos(user_id : int,
                           limit : int = 10,
                           offset : int = 0,
                           current_user : dict = Depends(require_role('admin')),
                           db : Session= Depends(get_db)):
    
    return todo_service.get_all_todos(current_user, db, user_id = user_id, limit= limit, offset=offset)
# ===============================================================================================================================
@router_admin.put('/update_todo/{todo_id}',response_model=TodoShowUpdate)
def endpoint_update_todo(todo_id:int,
                         new_todo : TodoUpdateAdmin,
                         current_user : dict = Depends(require_role('admin')),
                         db : Session= Depends(get_db)
                         ):
    return todo_service.update_todo(todo_id, new_todo, current_user, db)
   
# ===============================================================================================================================
@router_admin.get('/get_all_todos_with_owner/{user_id}', response_model=list[TodoShowWithOwner])
def endpoint_get_all_todos_with_owner(  user_id : int,
                                        limit : int = 10,
                                        offset : int = 0,
                                        current_user : dict = Depends(require_role('admin')),
                                        db : Session= Depends(get_db)):
    
    return todo_service.get_all_todos_with_username(current_user, db, user_id = user_id, limit= limit, offset=offset)    