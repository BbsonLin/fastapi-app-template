from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.utils import get_project_info
from app.config import settings

project_info = get_project_info()
# Application
app = FastAPI(title=project_info['name'], version=project_info['version'])
# Router
app.include_router(api_router)
# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CORS_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root(request: Request):
    # https://github.com/tiangolo/fastapi/issues/828#issuecomment-570965655
    return {"Swgger Document": f"{request.url._url}docs", "Redoc Document": f"{request.url._url}redoc"}
