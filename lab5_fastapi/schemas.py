from pydantic import BaseModel
from typing import List, Optional


# ----- Player -----

class PlayerBase(BaseModel):
    name: str
    position: str


class Player(PlayerBase):
    id: int

    class Config:
        orm_mode = True  # позволяет читать из SQLAlchemy-модели


# ----- Team -----

class TeamBase(BaseModel):
    location: str
    name: str
    mascot: Optional[str] = None


class Team(TeamBase):
    id: int
    players: List[Player] = []

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True