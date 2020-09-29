from fastapi import FastAPI, Request

from app.api import api_router


app = FastAPI()
app.include_router(api_router)


@app.get("/")
def root(request: Request):
    # https://github.com/tiangolo/fastapi/issues/828#issuecomment-570965655
    return {"Swgger Document": f"{request.url._url}docs", "Redoc Document": f"{request.url._url}redoc"}
