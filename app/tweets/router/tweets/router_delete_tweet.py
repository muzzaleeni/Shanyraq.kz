from fastapi import Depends, HTTPException, status

from app.utils import AppModel
from app.tweets.service import Service, get_service
from app.tweets.router.tweets import router


class DeleteTweetResponse(AppModel):
    message: str



@router.delete("/{tweet_id}", response_model=DeleteTweetResponse)
def delete_tweet(
    tweet_id: str,
    svc: Service = Depends(get_service)
) -> DeleteTweetResponse:

    # Delete the tweet by the provided ID and user ID
    deleted = svc.repository.delete_tweet(tweet_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet not found or you do not have permission to delete it"
        )

    return DeleteTweetResponse(message="Tweet deleted successfully")
