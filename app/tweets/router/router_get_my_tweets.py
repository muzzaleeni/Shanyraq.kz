from typing import List

from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router

class Tweet(AppModel):
    text: str

class GetMyTweetsResponse(AppModel):
    tweets: List[Tweet]


@router.get("/", response_model=GetMyTweetsResponse)
def get_my_tweets(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> GetMyTweetsResponse:
    user_id = jwt_data.user_id
    temp_tweets = svc.repository.get_tweet_by_user_id(user_id)

    return GetMyTweetsResponse(tweets=temp_tweets)
