from fastapi import Depends, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from app.tweets.service import Service, get_service
from app.tweets.router import router


class UpdateTweetRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.patch("/{tweet_id}")
def update_tweet(
    tweet_id: str,
    updated_data: UpdateTweetRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    # Extract the user ID from the JWT data
    user_id = jwt_data.user_id

    # Update the tweet with the new data
    success = svc.repository.update_tweet(tweet_id, updated_data.dict())

    if not success:
        raise HTTPException(status_code=500, detail="Failed to update tweet")

    # Return a success message
    return {"message": "Tweet updated successfully"}
