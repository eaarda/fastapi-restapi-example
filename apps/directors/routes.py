from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from ..database import get_db
from . import schemas, models
from apps.movies.schemas import Movie as MovieSchema
from apps.movies.models import Movie as MovieModel


router = APIRouter(
    tags = ["Directors"]
)


@router.get('/directors', response_model=List[schemas.Director])
def get_directors(db: Session = Depends(get_db)):
    directors = db.query(models.Director).all()
    return directors


@router.get('/directors/{director_id}', response_model=schemas.Director)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director


@router.post('/directors', response_model=schemas.Director, status_code=status.HTTP_201_CREATED)
def create_director(director: schemas.DirectorCreate, db: Session = Depends(get_db)):
    new_director = models.Director(name=director.name)
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return new_director


@router.put('/directors/{director_id}', response_model=schemas.Director)
def update_director(director_id: int, director_update: schemas.DirectorCreate, db: Session = Depends(get_db)):
    db_director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not db_director:
        raise HTTPException(status_code=404, detail="Director not found")
    db_director.name = director_update.name
    db.commit()
    db.refresh(db_director)
    return db_director


@router.delete('/directors/{director_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    db_director = db.query(models.Director).filter(models.Director.id == director_id).first()
    if not db_director:
        raise HTTPException(status_code=404, detail="Director not found")
    db.delete(db_director)
    db.commit()
    return None


@router.get('/directors/{director_id}/movies', response_model=List[MovieSchema])
def get_director_movies(director_id: int, db: Session = Depends(get_db)):
    if not db.query(models.Director).filter(models.Director.id == director_id).first():
        raise HTTPException(status_code=404, detail="Director not found")
    db_movies = db.query(MovieModel).filter(MovieModel.director_id == director_id).all()
    return db_movies