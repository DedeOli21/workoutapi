from fastapi import FastAPI
from workout_api.routes import api_router

app = FastAPI(title='workoutApi')
app.include_router(api_router)
