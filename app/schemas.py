from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    full_name: str
    name: str
    code: Optional[str]
    nickname: Optional[str]
    stadium: Optional[str]
    competition: Optional[str]
    website: Optional[str]
    twitter_handle: Optional[str]
    national_team: Optional[bool]
    year_formed: Optional[int]
    country: Optional[str]
    location: Optional[str]
    num_domestic_champions: Optional[int]


class TeamCreate(TeamBase):
    logo_url_small: Optional[str]
    logo_url_medium: Optional[str]
    logo_url_large: Optional[str]
    player_record_appearances: Optional[str]
    record_num_appearances: Optional[int]
    player_record_goals: Optional[str]
    record_num_goals: Optional[int]


class TeamResponse(TeamBase):
    logo_urls: Optional[List[Dict[str, str]]] = Field(nullable=True)
    record_appearances: Optional[Dict[str, str]] = Field(nullable=True)
    record_goals: Optional[Dict[str, str]] = Field(nullable=True)
    id: int

    class Config:
        orm_mode = True


class LogoResponse(BaseModel):
    logo_urls: List[Dict[str, str]] = Field(nullable=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
