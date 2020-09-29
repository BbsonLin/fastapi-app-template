from fastapi import FastAPI, Request

from app.api import api_router
from app.utils import get_project_info

project_info = get_project_info()
app = FastAPI(title=project_info['name'], version=project_info['version'])
app.include_router(api_router)


@app.get("/")
def root(request: Request):
    # https://github.com/tiangolo/fastapi/issues/828#issuecomment-570965655
    return {"Swgger Document": f"{request.url._url}docs", "Redoc Document": f"{request.url._url}redoc"}
