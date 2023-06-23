from fastapi import APIRouter
from .users import router as user_router
from .favorite_tweets import router as favorite_tweets_router

router = APIRouter()

router.include_router(user_router)
router.include_router(favorite_tweets_router)
