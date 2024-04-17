from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api.categories.models import CategoryModel
from workout_api.categories.schemas import CategoryIn, CategoryOut
from workout_api.contrib.depedencies import DatabaseDependency
from sqlalchemy.future import select

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

@router.get(
    '/', 
    summary='get all Categories',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryOut],
)
async def query(db_session: DatabaseDependency) -> list[CategoryOut]:
    categorias: list[CategoryOut] = (await db_session.execute(select(CategoryModel))).scalars().all()
    
    return categorias


@router.get(
    '/{id}', 
    summary='get a Category by id',
    status_code=status.HTTP_200_OK,
    response_model=CategoryOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoryOut:
    categoria: CategoryOut = (
        await db_session.execute(select(CategoryModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Category dont find by id: {id}'
        )
    
    return categoria