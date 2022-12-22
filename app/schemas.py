from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union


class LogoBase(BaseModel):
    logo_url_small: str
    logo_url_medium: str
    logo_url_large: str


class TeamBase(BaseModel):
    full_name: str
    name: str
    code: Optional[str]
    nickname: Optional[str]
    stadium: Optional[str]
    competition: Optional[str]
    urls: Union[LogoBase, None]
    website: Optional[str]
    twitter_handle: Optional[str]
    national_team: Optional[bool]
    year_formed: Optional[int]
    football_assosciation: Optional[str]


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LogoResponse(BaseModel):
    logo_urls: Union[LogoBase, None] = None
