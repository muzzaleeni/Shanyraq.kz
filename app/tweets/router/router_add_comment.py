from fastapi import Depends, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class CommentRequest(AppModel):
    text: str


class CommentResponse(AppModel):
    comment_id: str


@router.post("/{id}/comments", response_model=CommentResponse)
def add_comment_to_tweet(
    tweet_id: str,
    comment_data: CommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> CommentResponse:
    user_id = jwt_data.user_id

    # Check if the tweet exists
    if not svc.repository.get_tweet_by_tweet_id(tweet_id):
        raise HTTPException(status_code=404, detail="Tweet not found.")

    # Add the comment to the tweet
    comment_id = svc.repository.add_comment_to_tweet(tweet_id, user_id, comment_data.text)

    return CommentResponse(comment_id=comment_id)
