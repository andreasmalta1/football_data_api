from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


class TeamBase(BaseModel):
    full_name: str
    name: str
    code: Optional[str]
    nickname: Optional[str]
    stadium: Optional[str]
    competition: Optional[str]
    logo_url_small: Optional[str]
    logo_url_medium: Optional[str]
    logo_url_large: Optional[str]
    website: Optional[str]
    twitter_handle: Optional[str]
    national_team: Optional[bool]
    year_formed: Optional[int]
    country: Optional[str]


class TeamCreate(TeamBase):
    pass


class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class LogoResponse(BaseModel):
    logo_urls: List[Dict[str, None]]
