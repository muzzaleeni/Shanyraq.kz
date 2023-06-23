from fastapi import APIRouter
from .comments import router as comment_router
from .tweets import router as tweet_router

router = APIRouter()

router.include_router(comment_router)
router.include_router(tweet_router)
