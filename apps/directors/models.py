from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from apps.database import Base


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(50), nullable=False,index=True)

    movies = relationship("Movie", back_populates="director")