from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.config import client, env, fastapi_config
from app.utils import import_routers_from_folder

app = FastAPI(**fastapi_config)
router = APIRouter()


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

# Import routers from /app/auth/router
import_routers_from_folder("app.auth.router", router)
# Import routers from /app/tweets/router
import_routers_from_folder("app.tweets.router", router)

# Include the router in the FastAPI application
app.include_router(router)
