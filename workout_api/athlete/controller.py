from fastapi import APIRouter, status

from workout_api.contrib.depedencies import DatabaseDependency

router = APIRouter()

@router.post(path='/', summary='Create new athlete', status_code=status.HTTP_201_CREATED)

async def post(db_session: DatabaseDependency, athlete_in):
    pass