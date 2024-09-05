from uuid import UUID
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.task import Task
from models.task import CreateTaskModel, SearchTaskModel, UpdateTaskModel
from services import utils
from services import user as UserService
from services.exception import ResourceNotFoundError, InvalidInputError

def get_all_tasks(conds: SearchTaskModel, db: Session) -> List[Task]:
    query = select(Task)
    
    if conds.summary is not None:
        query = query.filter(Task.summary.like(f"{conds.summary}%"))
    if conds.description is not None:
        query = query.filter(Task.description.like(f"{conds.description}%"))
    if conds.status is not None:
        query = query.filter(Task.status == conds.status)
    query = query.filter(Task.priority >= conds.priority)
    
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_task_by_id(task_id: UUID, db: Session) -> Task:
    return db.scalars(select(Task).filter(Task.id == task_id)).first()

def create_task(data: CreateTaskModel, db: Session) -> Task:
    user = UserService.get_user_by_id(data.user_id, db)
    
    if user is None:
        raise InvalidInputError("Invalid user information")
    
    task = Task(**data.model_dump())
    
    task.created_at = utils.get_current_utc_time()
    task.updated_at = utils.get_current_utc_time()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def update_task_by_id(task_id: UUID, data: UpdateTaskModel, db: Session) -> Task:
    task = get_task_by_id(task_id, db)
    
    if task is None:
        raise ResourceNotFoundError()
    
    updated = False
    if data.summary is not None:
        task.summary = data.summary
        updated = True
    if data.description is not None:
        task.description = data.description
        updated = True
    if data.status is not None:
        task.status = data.status
        updated = True
    if data.priority is not None:
        task.priority = data.priority
        updated = True
    if updated:
        task.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(task)
    
    return task

def delete_task_by_id(task_id: UUID, db: Session) -> None:
    task = get_task_by_id(task_id, db)
    
    if task is None:
        raise ResourceNotFoundError()
    
    db.delete(task)
    db.commit()