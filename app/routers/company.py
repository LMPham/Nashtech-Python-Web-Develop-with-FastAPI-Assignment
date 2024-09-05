from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from entities.company import CompanyMode
from database import get_async_db_context, get_db_context
from models.company import CompanyModel, CompanyViewModel, SearchCompanyModel
from services import company as CompanyService
from services.exception import ResourceNotFoundError

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[CompanyViewModel])
async def get_all_companies(
    name: str = Query(default=None),
    description: str = Query(default=None),
    mode: CompanyMode = Query(default=None),
    rating: int = Query(ge=0, le=5, default=0),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context)
):
    conds = SearchCompanyModel(name, description, mode, rating, page, size)
    return CompanyService.get_all_companies(conds, db)

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def get_company_by_id(company_id: UUID, db: Session = Depends(get_db_context)):
    company = CompanyService.get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    return company

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def create_company(request: CompanyModel, db: Session = Depends(get_db_context)):
    return CompanyService.create_company(request, db)

@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company_by_id(
    company_id: UUID,
    request: CompanyModel,
    db: Session = Depends(get_db_context)
):
    return CompanyService.update_company_by_id(company_id, request, db)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_by_id(company_id: UUID, db: Session = Depends(get_db_context)):
    CompanyService.delete_company_by_id(company_id, db)