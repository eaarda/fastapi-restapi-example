import json
from sqlalchemy.orm import Session

from apps.directors.models import Director as DirectorModel
from apps.movies.models import Movie as MovieModel


def insert_movie_database(db: Session):

    with open('movies.json') as f:
        data = json.load(f)
    
    for item in data:
        director_name = item['director']
        director = db.query(DirectorModel).filter(DirectorModel.name == director_name).first()

        if not director: 
            # Create a new director if not found in the database
            director = DirectorModel(name=director_name)
            db.add(director)
            db.commit()
            db.refresh(director)
        
        # Extract genre, year, rating, and runtime from the item
        genre = item['genre'].split(',')[0].strip() if item['genre'] else None
        year = int(item['year']) if 'year' in item else None
        rating = float(item['rating']) if 'rating' in item else None
        runtime = int(item['runtime'].split()[0]) if 'runtime' in item else None
        
        # Check if a movie with the same attributes already exists
        existing_movie = db.query(MovieModel).filter(
            MovieModel.title == item['title'],
            MovieModel.year == year,
            MovieModel.runtime == runtime,
            MovieModel.genre == genre,
            MovieModel.rating == rating
        ).first()

        if not existing_movie:
            # Create a new movie if it doesn't exist
            movie = MovieModel(
                title=item['title'],
                year=year,
                runtime=runtime,
                genre=genre,
                rating=rating,
                director_id=director.id
            )
            db.add(movie)
            db.commit()
            db.refresh(movie)

    return {"message": "Movies inserted successfully"}