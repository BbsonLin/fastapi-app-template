from fastapi import APIRouter


router = APIRouter()


@router.get('')
async def get_api_sample():
    return {'message': 'This is sample API'}
