import os
from typing import List
from fastapi import Depends, HTTPException, File, UploadFile
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from pydantic import BaseModel
from ..service import Service, get_service
from . import router


class CreateTweetRequest(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class CreateTweetResponse(BaseModel):
    tweet_id: str

@router.post("/", response_model=CreateTweetResponse)
def create_tweet(
        tweet_data: CreateTweetRequest,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service)
) -> CreateTweetResponse:
    # Extract the user ID from the JWT data
    user_id = jwt_data.user_id
    # Create a new ad with the provided data
    temp_tweet_id: str = svc.repository.create_tweet(user_id, tweet_data.dict())

    if not temp_tweet_id:
        raise HTTPException(status_code=500, detail="Failed to create tweet")

    # Return the ID of the created ad
    return CreateTweetResponse(tweet_id=temp_tweet_id)


