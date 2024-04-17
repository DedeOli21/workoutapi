from datetime import datetime
from sqlalchemy import Integer, String
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TeamModel(BaseModel):
    __tablename__ = 'teams'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    local: Mapped[str] = mapped_column(String(20), nullable=True)
    manager: Mapped[str] = mapped_column(String(30), nullable=True)
    athlete: Mapped['AthleteModel'] = relationship(back_populates='team')
