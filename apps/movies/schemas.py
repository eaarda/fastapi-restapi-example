from pydantic import BaseModel
from typing import Optional

from apps.directors.schemas import Director


class MovieBase(BaseModel):
    title: str
    year: Optional[int]
    rating: Optional[float]
    runtime: Optional[int]
    genre: Optional[str]
    director_id: int

class MovieCreate(MovieBase):
    title: str
    year: Optional[int]
    rating: Optional[float]
    runtime: Optional[int]
    genre: Optional[str]
    director_id: int

class Movie(MovieBase):
    id: int
    director: Director 

    class Config:
        orm_mode = True