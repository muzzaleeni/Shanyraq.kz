from fastapi import APIRouter
from app.tweets.router.comments import router as comment_router
from app.tweets.router.tweets import router as tweet_router

router = APIRouter()

router.include_router(comment_router)
router.include_router(tweet_router)
