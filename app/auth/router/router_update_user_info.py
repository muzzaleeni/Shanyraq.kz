from fastapi import Depends, HTTPException
from pydantic import BaseModel
from . import router
from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from .dependencies import parse_jwt_user_data


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
