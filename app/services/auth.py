from datetime import timedelta
from enum import Enum
from typing import Annotated, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
import jwt

from entities.user import User, verify_password
from models.auth import UserClaims
from services.exception import UnAuthorizedError
from services.utils import get_current_timestamp
from settings import COGNITO, JWT_SECRET, JWT_ALGORITHM


class LocalAuthorizer:
    security_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
    
    def __init__(self) -> None:
        pass

    def __call__(self, token: Annotated[str, Depends(security_scheme)] = None):
        if not token:
            raise UnAuthorizedError()
        
        try:
            claims = jwt.decode(
                token,
                key=JWT_SECRET,
                algorithms=[JWT_ALGORITHM],
                options={
                    "verify_aud": False,
                    "verify_iss": False,
                    "verify_exp": True,
                }
            )
            return UserClaims(**claims)

        except jwt.PyJWTError as err:
            print(err)
            raise UnAuthorizedError()

class CognitoTokenType(Enum):
    ID_TOKEN = "id_token"
    ACCESS_TOKEN = "access_token"

class CognitoAuthorizer:
    security_scheme = HTTPBearer(
        scheme_name="Bearer",
        bearerFormat="JWT",
        description="Bearer token for Cognito",
    )

    def __init__(self, token_type: CognitoTokenType = CognitoTokenType.ID_TOKEN) -> None:
        self.token_type = token_type
        self.client_id = COGNITO["CLIENT_ID"]
        self.jwks_client = jwt.PyJWKClient(
            uri=COGNITO["JWKS_URL"],
            cache_keys=True
        )

    def __call__(self, authorization: Annotated[HTTPAuthorizationCredentials | None, Depends(security_scheme)] = None) -> UserClaims:
        if not authorization:
            raise UnAuthorizedError()

        token = authorization.credentials

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            claims = jwt.decode(
                token, 
                signing_key.key, 
                algorithms=[signing_key.algorithm_name],
                audience=self.client_id,
                options={
                    "verify_exp": True,
                    "verify_signature": True,
                    "verify_aud": True,
                }
            )
            user = UserClaims(**claims)
            user.username = claims.get("cognito:username", None)
            user.is_staff = bool(claims.get("custom:is_staff", False))
            print(user)
            return user
        except jwt.PyJWKClientConnectionError:
            print("Cannot connect to JWKS URL")
            raise UnAuthorizedError()
        except jwt.PyJWKError as err:
            print(err)
            raise jwt.InvalidTokenError()

authorizer = CognitoAuthorizer() if COGNITO["ENABLED"] else LocalAuthorizer()

def create_access_token(user: User, expires: Optional[int] = None):
    claims = UserClaims(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        email_verified=True,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        is_admin=user.is_admin,
        aud='FastAPI',
        iss='FastAPI',
        iat=get_current_timestamp(),
        exp=get_current_timestamp() + expires if expires else get_current_timestamp() + int(timedelta(minutes=10).total_seconds())
    )
    return jwt.encode(claims.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)

def authenticate_user(username: str, password: str, db: Session):
    user = db.scalars(select(User).filter(User.username == username)).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user