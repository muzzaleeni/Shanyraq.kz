from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.service import Service, get_service
from app.auth.router.dependencies import parse_jwt_user_data
from pydantic import BaseModel
from app.auth.router.users import router


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
