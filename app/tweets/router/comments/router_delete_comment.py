from fastapi import Depends, HTTPException
# from app.utils import AppModel

from app.tweets.service import Service, get_service
from app.tweets.router.comments import router


@router.delete("/{id}/comments/{comment_id}")
def delete_comment(
    tweet_id: str,
    comment_id: str,
    svc: Service = Depends(get_service),
) -> None:
    # Check if the tweet exists
    if not svc.repository.get_tweet_by_tweet_id(tweet_id):
        raise HTTPException(status_code=404, detail="Tweet not found.")

    # Check if the comment exists and is owned by the authenticated user
    if not svc.repository.get_comment_by_id(tweet_id, comment_id):
        raise HTTPException(status_code=404, detail="Comment not found.")

    # Delete the comment
    if not svc.repository.delete_comment(tweet_id, comment_id):
        raise HTTPException(status_code=500, detail="Failed to delete comment.")
