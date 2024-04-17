from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from workout_api.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship


class AthleteModel(BaseModel):
    __tablename__ = 'athletes'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    country: Mapped[str] = mapped_column(String(30), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    height: Mapped[float] = mapped_column(Float, nullable=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)
    category: Mapped['CategoryModel'] = relationship(back_populates='athlete', lazy='selectin')
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.pk_id'))
    team: Mapped['TeamModel'] = relationship(back_populates='athlete', lazy='selectin')
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.pk_id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)