from pydantic import BaseModel


class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    name: str

class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True