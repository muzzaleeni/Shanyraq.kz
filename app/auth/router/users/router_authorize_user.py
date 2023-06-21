from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.auth.service import Service, get_service
from app.auth.utils.security import check_password
from app.auth.router.users import router
from app.auth.router.errors import InvalidCredentialsException


class AuthorizeUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/tokens", response_model=AuthorizeUserResponse)
def authorize_user(
    input: OAuth2PasswordRequestForm = Depends(),
    svc: Service = Depends(get_service),
) -> AuthorizeUserResponse:
    user = svc.repository.get_user_by_email(input.username)

    if not user:
        raise InvalidCredentialsException

    if not check_password(input.password, user["password"]):
        raise InvalidCredentialsException

    return AuthorizeUserResponse(
        access_token=svc.jwt_svc.create_access_token(user=user),
    )
