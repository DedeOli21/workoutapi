from typing import Annotated

from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema

class CategoryIn(BaseSchema):
    name: Annotated[str, Field(description='Name of Categories', examples={'liveWeight'}, max_length=50)]

class CategoryOut(CategoryIn):
    id: Annotated[UUID4, Field(description='Id of categorie')]