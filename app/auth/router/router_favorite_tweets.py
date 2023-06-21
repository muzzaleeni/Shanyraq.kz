from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.auth.service import Service as Auth_Service, get_service as auth_get_service
from app.tweets.service import Service as Tweet_Service, get_service as tweet_get_service
from app.auth.router import router


@router.get("/favorites/{tweet_id}")
def add_tweet_to_favorites(
        tweet_id: str,
        jwt_data: JWTData = Depends(parse_jwt_user_data),
        auth_svc: Auth_Service = Depends(auth_get_service),
        tweet_svc: Tweet_Service = Depends(tweet_get_service)
):
    user_id = jwt_data.user_id

    # Check if the tweet exists
    tweet = tweet_svc.repository.get_tweet_by_tweet_id(tweet_id)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")

    # Add the tweet to the user's favorite tweets
    auth_svc.repository.add_tweet_to_favorites(user_id, tweet_id)

    return {"message": "Tweet added to favorite tweets"}
