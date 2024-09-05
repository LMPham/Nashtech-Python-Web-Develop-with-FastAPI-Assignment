from uuid import UUID
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from entities.company import CompanyMode
from database import get_db_context
from models.auth import UserClaims
from models.company import CreateCompanyModel, CompanyViewModel, UpdateCompanyModel, SearchCompanyModel
from services import company as CompanyService
from services.auth import authorizer
from services.exception import ResourceNotFoundError, AccessDeniedError

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", status_code=status.HTTP_200_OK, response_model=list[CompanyViewModel])
async def get_all_companies(
    name: str = Query(default=None),
    description: str = Query(default=None),
    mode: CompanyMode = Query(default=None),
    rating: int = Query(ge=0, le=5, default=0),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=50, default=10),
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    conds = SearchCompanyModel(name, description, mode, rating, page, size)
    return CompanyService.get_all_companies(conds, db)

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def get_company_by_id(
    company_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active:
        raise AccessDeniedError()
    
    company = CompanyService.get_company_by_id(company_id, db)
    
    if company is None:
        raise ResourceNotFoundError()
    
    return company

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CompanyViewModel)
async def create_company(
    request: CreateCompanyModel, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return CompanyService.create_company(request, db)

@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyViewModel)
async def update_company_by_id(
    company_id: UUID,
    request: UpdateCompanyModel,
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    return CompanyService.update_company_by_id(company_id, request, db)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_by_id(
    company_id: UUID, 
    db: Session = Depends(get_db_context),
    userClaim: UserClaims = Depends(authorizer)
):
    if not userClaim.is_active or not userClaim.is_admin:
        raise AccessDeniedError()
    
    CompanyService.delete_company_by_id(company_id, db)