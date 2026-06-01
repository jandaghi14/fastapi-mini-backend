from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from datetime import datetime


from app.infrastructure.models import Todo


def create_todo_db(new_todo, current_user_id, db: Session):
    try:
        todo = Todo(
            title=new_todo.title,
            description=new_todo.description,
            priority=new_todo.priority,
            due_date=new_todo.due_date,
            user_id=current_user_id

        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        db.rollback()
        raise e


def get_todo_by_id_db(todo_id, db: Session, include_deleted: bool = False):
    if include_deleted:
        return db.query(Todo).filter(Todo.id == todo_id).first()
    return db.query(Todo).filter(Todo.id == todo_id, Todo.is_deleted.is_(False)).first()


def hard_delete_todo_db(todo: Todo, db: Session):

    db.delete(todo)
    db.commit()
    return True


def soft_delete_todo_db(todo: Todo, db: Session):
    todo.is_deleted = True
    db.commit()
    db.refresh(todo)
    return True


def get_all_todos_db(
    db: Session,
    user_id: int,
    limit=10,
    offset=0,
    include_deleted: bool = False,
    due_date_from: datetime = None,
):
    query = db.query(Todo).filter(Todo.user_id == user_id)

    if not include_deleted:
        query = query.filter(Todo.is_deleted.is_(False))

    if due_date_from is not None:
        query = query.filter(Todo.due_date >= due_date_from)

    return query.limit(limit).offset(offset).all()


def update_todo_db(old_todo, new_todo, db: Session, is_admin: bool = False):
    if is_admin:
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


def get_all_todos_with_username_db(
        current_user: int,
        db: Session,
        limit=10,
        offset=0,
        due_date_from: datetime = None,
        include_deleted: bool = False):
    query = db.query(Todo).options(joinedload(Todo.owner)).filter(Todo.user_id == current_user)

    if not include_deleted:
        query = query.filter(Todo.is_deleted.is_(False))

    if due_date_from is not None:
        query = query.filter(Todo.due_date >= due_date_from)

    return query.limit(limit).offset(offset).limit(limit).offset(offset).all()
