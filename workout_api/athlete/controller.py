from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy.future import select
from datetime import datetime
from workout_api.athlete.models import AthleteModel
from workout_api.athlete.schemas import AthleteIn, AthleteOut, AthleteUpdate
from workout_api.categories.models import CategoryModel
from workout_api.team.models import TeamModel
from workout_api.contrib.depedencies import DatabaseDependency
from pydantic import UUID4
from uuid import uuid4

router = APIRouter()

@router.post(
    '/', 
    summary='Create a new athlete',
    status_code=status.HTTP_201_CREATED,
    response_model=AthleteOut
)
async def post(
    db_session: DatabaseDependency, 
    athlete_in: AthleteIn = Body(...)
):
    category_name = athlete_in.category.name
    team_name = athlete_in.team.name

    category = (await db_session.execute(
        select(CategoryModel).filter_by(nome=category_name))
    ).scalars().first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'The category {category_name} dont find.'
        )
    
    team = (await db_session.execute(
        select(TeamModel).filter_by(nome=team_name))
    ).scalars().first()
    
    if not team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'the team {team_name} dont find.'
        )
    try:
        athlete_out = AthleteOut(id=uuid4(), created_at=datetime.utcnow(), **athlete_in.model_dump())
        athlete_model = AthleteModel(**athlete_out.model_dump(exclude={'category', 'team'}))

        athlete_model.category_id = category.pk_id
        athlete_model.team_id = team.pk_id
        
        db_session.add(athlete_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Something goes wrong!!'
        )

    return athlete_out


@router.get(
    '/', 
    summary='Get All Athletes',
    status_code=status.HTTP_200_OK,
    response_model=list[AthleteOut],
)
async def query(db_session: DatabaseDependency) -> list[AthleteOut]:
    athletes: list[AthleteOut] = (await db_session.execute(select(AthleteModel))).scalars().all()
    
    return [AthleteOut.model_validate(athlete) for athlete in athletes]


@router.get(
    '/{id}', 
    summary='get a Athlete by id',
    status_code=status.HTTP_200_OK,
    response_model=AthleteOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AthleteOut:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id=id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Athlete dont find by id: {id}'
        )
    
    return athlete


@router.patch(
    '/{id}', 
    summary='Edit a athlete by id',
    status_code=status.HTTP_200_OK,
    response_model=AthleteOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AthleteUpdate = Body(...)) -> AthleteOut:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id=id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Athlete dont find by id: {id}'
        )
    
    athlete_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in athlete_update.items():
        setattr(athlete, key, value)

    await db_session.commit()
    await db_session.refresh(athlete)

    return athlete


@router.delete(
    '/{id}', 
    summary='delete a athlete by id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id=id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'athlete dont find by id: {id}'
        )
    
    await db_session.delete(athlete)
    await db_session.commit()