from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema

class TeamIn(BaseSchema):
    name: Annotated[str, Field(description='Name of Team', examples={'Mata Leao'}, max_length=20)]
    local: Annotated[str, Field(description='local of Team', examples={'Brazil'}, max_length=20)]
    manager: Annotated[str, Field(description='manager of Team', examples={'Glover Teixeira'}, max_length=30)]


class TeamAthlete(BaseSchema):
    nome: Annotated[str, Field(description='Name of team', example='Mata Leao', max_length=20)]


class TeamOut(TeamIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]   