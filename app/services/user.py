from uuid import UUID
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from entities.user import User, get_password_hash
from models.user import CreateUserModel, SearchUserModel, UpdateUserModel
from services import utils
from services import company as CompanyService
from services.exception import ResourceNotFoundError, InvalidInputError

def get_all_users(conds: SearchUserModel, db: Session) -> List[User]:
    query = select(User)
    
    if conds.email is not None:
        query = query.filter(User.email.like(f"{conds.email}%"))
    if conds.username is not None:
        query = query.filter(User.username.like(f"{conds.username}%"))
    if conds.first_name is not None:
        query = query.filter(User.first_name.like(f"{conds.first_name}%"))
    if conds.last_name is not None:
        query = query.filter(User.last_name.like(f"{conds.last_name}%"))
    if conds.is_active is not None:
        query = query.filter(User.is_active == conds.is_active)
    if conds.is_admin is not None:
        query = query.filter(User.is_admin == conds.is_admin)
    
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_user_by_id(user_id: UUID, db: Session) -> User:
    return db.scalars(select(User).filter(User.id == user_id)).first()

def get_user_by_company_id_and_username(company_id: UUID, username: str, db: Session) -> User:
    return db.scalars(select(User).filter(and_(User.company_id == company_id, User.username == username))).first()

def create_user(data: CreateUserModel, db: Session) -> User:
    company = CompanyService.get_company_by_id(data.company_id, db)
    
    if company is None:
        raise InvalidInputError("Invalid company information")
    
    user = User(**data.model_dump())
    
    # Generate unique username based on first and last name
    user.username = f"{user.first_name}.{user.last_name}"
    user.username = format(user.username)
    salt = 1
    while get_user_by_company_id_and_username(user.company_id, user.username, db) is not None:
        user.username = f"{user.first_name}.{user.last_name}{salt}"
        user.username = format(user.username)
        salt += 1
    user.username = format(user.username)
    user.email= f"{user.username}@{company.name}.com"
    user.email = format(user.email)
    user.hashed_password = get_password_hash(f"{user.username}@password")
    
    user.created_at = utils.get_current_utc_time()
    user.updated_at = utils.get_current_utc_time()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def update_user_by_id(user_id: UUID, data: UpdateUserModel, db: Session) -> User:
    user = get_user_by_id(user_id, db)
    
    if user is None:
        raise ResourceNotFoundError()
    
    updated = False
    if data.password is not None:
        user.hashed_password = get_password_hash(data.password)
        updated = True
    if data.is_active is not None:
        user.is_active = data.is_active
        updated = True
    if data.is_admin is not None:
        user.is_admin = data.is_admin
        updated = True
    if updated:
        user.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(user)
    
    return user

def delete_user_by_id(user_id: UUID, db: Session) -> None:
    user = get_user_by_id(user_id, db)
    
    if user is None:
        raise ResourceNotFoundError()
    
    db.delete(user)
    db.commit()
    
def format(str) -> str:
    return str.replace(" ", "").lower()