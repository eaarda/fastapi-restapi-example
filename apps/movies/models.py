from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from apps.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(80), nullable=False, index=True)
    genre = Column(String(80), index=True)
    director_id = Column(Integer,ForeignKey('directors.id'),nullable=False)
    year = Column(Integer, index=True)
    rating = Column(Float, index=True)
    runtime = Column(Integer, index=True)

    director = relationship("Director", back_populates="movies")