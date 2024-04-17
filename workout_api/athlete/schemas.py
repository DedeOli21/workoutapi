from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categories.schemas import CategoryIn
from workout_api.team.schemas import TeamAthlete

class Athlete(BaseSchema):
    name: Annotated[str, Field(description='Name of Athlete', examples={'Alex Pereira'}, max_length=50)]
    country: Annotated[str, Field(description='Country of Athlete', examples={'Brazul'}, max_length=30)]
    age: Annotated[int, Field(description='age of Athlete', examples={25})]
    weight: Annotated[PositiveFloat, Field(description='weight of Athlete', examples={93.5})]
    height: Annotated[PositiveFloat, Field(description='widht of Athlete', examples={1.90})]
    gender: Annotated[str, Field(description='gender of Athlete', examples={'M'}, max_length=1)]
    category: Annotated[CategoryIn, Field(description='category of Athlete', examples={'live weight'}, max_length=20)]
    team: Annotated[TeamAthlete, Field(description='category of Athlete', examples={'live weight'}, max_length=20)]


class AthleteIn(Athlete):
    pass


class AthleteOut(Athlete, OutMixin):
    pass

class AthleteUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Name of Athlete', example='Poatan', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='age of Athlete', example=25)]