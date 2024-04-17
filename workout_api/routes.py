from fastapi import APIRouter
from workout_api.athlete.controller import router as athleteRouter
from workout_api.categories.controller import router as categoriesRouter
from workout_api.team.controller import router as teamsRouter

api_router = APIRouter()
api_router.include_router(athleteRouter, prefix='/athletes', tags=['athletes'])
api_router.include_router(categoriesRouter, prefix='/categories', tags=['categories'])
api_router.include_router(teamsRouter, prefix='/teams', tags=['teams'])