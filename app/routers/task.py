from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from entities.task import TaskStatus
from database import get_db_context
from models.auth import UserClaims
from models.task import CreateTaskModel, TaskViewModel, UpdateTaskModel, SearchTaskModel
from services import task as TaskService
from services.auth import authorizer
from services.exception import ResourceNotFoundError, AccessDeniedError

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[TaskViewModel])
async def get_all_tasks(
    summary: str = Query(default=None),
    description: str = Query(default=None),
    status: TaskStatus = Query(default=None),
    priority: int = Query(ge=0, le=5, default=0),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    conds = SearchTaskModel(summary, description, status, priority, page, size)
    return TaskService.get_all_tasks(conds, db)

@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def get_task_by_id(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    task = TaskService.get_task_by_id(task_id, db)
    
    if task is None:
        raise ResourceNotFoundError()
    
    return task

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskViewModel)
async def create_task(
    request: CreateTaskModel,
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return TaskService.create_task(request, db)

@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskViewModel)
async def update_task_by_id(
    task_id: UUID,
    request: UpdateTaskModel,
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return TaskService.update_task_by_id(task_id, request, db)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(
    task_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    TaskService.delete_task_by_id(task_id, db)