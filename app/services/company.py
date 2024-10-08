from uuid import UUID
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session

from entities.company import Company
from models.company import CreateCompanyModel, SearchCompanyModel, UpdateCompanyModel
from services import utils
from services.exception import ResourceNotFoundError

def get_all_companies(conds: SearchCompanyModel, db: Session) -> List[Company]:
    query = select(Company)
    
    if conds.name is not None:
        query = query.filter(Company.name.like(f"{conds.name}%"))
    if conds.description is not None:
        query = query.filter(Company.description.like(f"{conds.description}%"))
    if conds.mode is not None:
        query = query.filter(Company.mode == conds.mode)
    query = query.filter(Company.rating >= conds.rating)
    
    query = query.offset((conds.page-1)*conds.size).limit(conds.size)
    
    return db.scalars(query).all()

def get_company_by_id(company_id: UUID, db: Session) -> Company:
    return db.scalars(select(Company).filter(Company.id == company_id)).first()

def create_company(data: CreateCompanyModel, db: Session) -> Company:
    company = Company(**data.model_dump())
    
    company.created_at = utils.get_current_utc_time()
    company.updated_at = utils.get_current_utc_time()
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return company

def update_company_by_id(company_id: UUID, data: UpdateCompanyModel, db: Session) -> Company:
    company = get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    updated = False
    if data.name is not None:
        company.name = data.name
        updated = True
    if data.description is not None:
        company.description = data.description
        updated = True
    if data.mode is not None:
        company.mode = data.mode
        updated = True
    if data.rating is not None:
        company.rating = data.rating
        updated = True
    if updated:
        company.updated_at = utils.get_current_utc_time()
    
    db.commit()
    db.refresh(company)
    
    return company

def delete_company_by_id(company_id: UUID, db: Session) -> None:
    company = get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    db.delete(company)
    db.commit()