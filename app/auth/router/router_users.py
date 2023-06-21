from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.auth.service import Service, get_service
from app.auth.utils.security import check_password
from app.auth.router import router
from app.auth.router.errors import InvalidCredentialsException


# Authorize user
class AuthorizeUserResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


@router.post("/", response_model=AuthorizeUserResponse)
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


# Register user

class RegisterUserRequest(BaseModel):
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    email: str


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserResponse
)
def register_user(
        input: RegisterUserRequest,
        svc: Service = Depends(get_service),
) -> RegisterUserResponse:
    if svc.repository.get_user_by_email(input.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )

    svc.repository.create_user(input.dict())

    return RegisterUserResponse(email=input.email)


# Get user info
class GetMyAccountResponse(BaseModel):
    id: str
    email: str
    phone: str
    name: str
    city: str


@router.get("/me", response_model=GetMyAccountResponse)
def get_my_account(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
) -> GetMyAccountResponse:
    user_id = jwt_data.user_id

    # Retrieve the user from the service or repository
    user = svc.repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user data
    return GetMyAccountResponse(
        id=str(user["_id"]),
        email=user["email"],
        phone=user.get("phone", ""),
        name=user.get("name", ""),
        city=user.get("city", "")
    )


class UpdateUserDataRequest(BaseModel):
    email: str
    phone: str
    name: str
    city: str


class UpdateUserDataResponse(BaseModel):
    email: str
    phone: str
    name: str
    city: str


# Update user info
@router.patch("/me", response_model=UpdateUserDataResponse)
def update_user_data(
        user_data: UpdateUserDataRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service)
) -> UpdateUserDataResponse:
    user_id = jwt_data.user_id

    # Retrieve the user from the service or repository
    user = svc.repository.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's data
    user["email"] = user_data.email
    user["phone"] = user_data.phone
    user["name"] = user_data.name
    user["city"] = user_data.city

    # Save the updated user to the repository
    svc.repository.update_user(user)
    return UpdateUserDataResponse(email=user["email"], phone=user["phone"], name=user["name"], city=user["city"])
