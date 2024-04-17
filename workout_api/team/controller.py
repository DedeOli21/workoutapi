from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from workout_api.team.schemas import TeamIn, TeamOut
from workout_api.team.models import TeamModel

from workout_api.contrib.depedencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/', 
    summary='Create a new team',
    status_code=status.HTTP_201_CREATED,
    response_model=TeamOut,
)
async def post(
    db_session: DatabaseDependency, 
    team_in: TeamIn = Body(...)
) -> TeamOut:
    team_out = TeamOut(id=uuid4(), **team_in.model_dump())
    team_model = TeamModel(**team_out.model_dump())
    
    db_session.add(team_model)
    await db_session.commit()

    return team_out
    
    
@router.get(
    '/', 
    summary='getAll team',
    status_code=status.HTTP_200_OK,
    response_model=list[TeamOut],
)
async def query(db_session: DatabaseDependency) -> list[TeamOut]:
    team_out: list[TeamOut] = (
        await db_session.execute(select(TeamModel))
    ).scalars().all()
    
    return team_out


@router.get(
    '/{id}', 
    summary='get team by id',
    status_code=status.HTTP_200_OK,
    response_model=TeamOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> TeamOut:
    team_out: TeamOut = (
        await db_session.execute(select(TeamModel).filter_by(id=id))
    ).scalars().first()

    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'team not found by id: {id}'
        )
    
    return team_out