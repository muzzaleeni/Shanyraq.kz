from fastapi import Depends, HTTPException
from app.utils import BaseModel
from ..service import Service, get_service
from . import router


class GetTweetResponse(BaseModel):
    _id: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str


@router.get("/{id}", response_model=GetTweetResponse)
def get_tweet(
    id: str,
    svc: Service = Depends(get_service)
) -> GetTweetResponse:
    # Retrieve the tweet from the service or repository
    tweet = svc.repository.get_tweet_by_tweet_id(id)

    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Return the tweet data
    return GetTweetResponse(
        _id=tweet["_id"],
        type=tweet["type"],
        price=tweet["price"],
        address=tweet["address"],
        area=tweet["area"],
        rooms_count=tweet["rooms_count"],
        description=tweet["description"],
        user_id=tweet["created_by"],
    )
