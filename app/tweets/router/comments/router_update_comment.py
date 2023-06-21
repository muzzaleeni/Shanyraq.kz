from fastapi import Depends, HTTPException
# from app.auth.adapters.jwt_service import JWTData
# from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from app.tweets.service import Service, get_service
from app.tweets.router.comments import router


class UpdateCommentRequest(AppModel):
    text: str


@router.patch("/{tweet_id}/comments/{comment_id}")
def update_comment_text(
        tweet_id: str,
        comment_id: str,
        comment_data: UpdateCommentRequest,
        # jwt_data: JWTData = Depends(parse_jwt_user_data),
        svc: Service = Depends(get_service),
) -> None:
    # Check if the tweet exists
    if not svc.repository.get_tweet_by_tweet_id(tweet_id):
        raise HTTPException(status_code=404, detail="Tweet not found.")

    # Check if the comment exists and is owned by the authenticated user
    # user_id = jwt_data.user_id
    if not svc.repository.get_comment_by_id(tweet_id, comment_id):
        raise HTTPException(status_code=404, detail="Comment not found.")

    # Update the comment text
    updated_data = {"text": comment_data.text}
    if not svc.repository.update_comment(tweet_id, comment_id, updated_data):
        raise HTTPException(status_code=500, detail="Failed to update comment.")
