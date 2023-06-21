from fastapi import Depends, HTTPException
from typing import List

# from app.auth.adapters.jwt_service import JWTData
# from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from app.tweets.service import Service, get_service
from app.tweets.router import router


class GetTweetCommentsResponse(AppModel):
    comments: List


@router.get("/{id}/comments", response_model=GetTweetCommentsResponse)
def get_tweet_comments(
        tweet_id: str,
        # jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
) -> GetTweetCommentsResponse:
    # Check if the tweet exists
    if not svc.repository.get_tweet_by_tweet_id(tweet_id):
        raise HTTPException(status_code=404, detail="Tweet not found.")

    # Get the comments for the tweet
    comments = svc.repository.get_tweet_comments(tweet_id)

    return GetTweetCommentsResponse(comments=comments)
