from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import client, env, fastapi_config

from app.auth.router import router as auth_router
from app.tweets.router import router as tweets_router


app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

# Include the routes from the auth_router
app.include_router(auth_router, prefix="/auth", tags=["Users"])

# Include the routes from the tweets_router
app.include_router(tweets_router, prefix="/tweets", tags=["Tweets"])
