from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TeamBase(BaseModel):
    name: str
    url: Optional[str]


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    url: str


class TeamResponse(TeamBase):
    id: int
    name: str
    url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
