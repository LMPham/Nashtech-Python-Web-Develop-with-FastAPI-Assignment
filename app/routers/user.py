from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_context
from models.user import CreateUserModel, UserViewModel, UpdateUserModel, SearchUserModel
from models.auth import UserClaims
from services import user as UserService
from services.auth import authorizer
from services.exception import ResourceNotFoundError, AccessDeniedError

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserViewModel])
async def get_all_users(
    email: str = Query(default=None),
    username: str = Query(default=None),
    first_name: str = Query(default=None),
    last_name: str = Query(default=None),
    is_active: bool = Query(default=None),
    is_admin: bool = Query(default=None),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    conds = SearchUserModel(email, username, first_name, last_name, is_active, is_admin, page, size)
    return UserService.get_all_users(conds, db)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def get_user_by_id(
    user_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    user = UserService.get_user_by_id(user_id, db)
    
    if user is None:
        raise ResourceNotFoundError()
    
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserViewModel)
async def create_user(
    request: CreateUserModel, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return UserService.create_user(request, db)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserViewModel)
async def update_user_by_id(
    user_id: UUID,
    request: UpdateUserModel,
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return UserService.update_user_by_id(user_id, request, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    UserService.delete_user_by_id(user_id, db)