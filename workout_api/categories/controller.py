from uuid import uuid4
from fastapi import APIRouter, Body, status

from workout_api.categories.models import CategoryModel
from workout_api.categories.schemas import CategoryIn, CategoryOut
from workout_api.contrib.depedencies import DatabaseDependency

router = APIRouter()

@router.post(path='/', summary='Create new category', status_code=status.HTTP_201_CREATED)
async def post(
    db_session: DatabaseDependency, 
    category_in: CategoryIn = Body(...)
    ) -> CategoryOut:
    category_out = CategoryOut(id=uuid4(), **category_in.model_dump())

    categoy_model = CategoryModel(**category_out.model_dump())

    db_session.add(categoy_model)
    await db_session.commit()

    return category_out