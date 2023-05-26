import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from imdb import insert_movie_database
from apps.database import engine, get_db

# Models
from apps.directors import models as directors_models
from apps.movies import models as movies_models

# Routes
from apps.movies.routes import router as movies_router
from apps.directors.routes import router as directors_router


app = FastAPI(title="BursaBilisimToplulugu - Rest API Example", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Bad Request"})


@app.on_event("startup")
def startup():
    # Create database tables on startup
    directors_models.Base.metadata.create_all(bind=engine)
    movies_models.Base.metadata.create_all(bind=engine)


@app.get("api/v1/imdb-database", tags=["IMDB"], summary="IMDB Database Initialization", description="This endpoint initializes the IMDB database.")
async def root(db: Session = Depends(get_db)):
    # Endpoint to initialize the IMDB database
    return insert_movie_database(db)


# Routes
routers = [movies_router, directors_router]
for router in routers:
    app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)