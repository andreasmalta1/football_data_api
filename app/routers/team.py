from fastapi import status, APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import random

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    import schemas
    import models
    import oauth2


router = APIRouter(prefix="/teams", tags=["Teams"])

FIELDS = [
    "id",
    "full_name",
    "name",
    "code",
    "nickname",
    "stadium",
    "competition",
    "website",
    "twitter_handle",
    "national_team",
    "year_formed",
    "country",
    "num_domestic_champions",
    "created_at",
]

LOGO_FIELDS = ["logo_url_small", "logo_url_medium", "logo_url_large"]

APP_FIELDS = ["player_record_appearances", "record_num_appearances"]

GOAL_FIELDS = ["player_record_goals", "record_num_goals"]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TeamResponse,
    include_in_schema=False,
)
def create_team(
    team: schemas.TeamCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    new_team = models.Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    results = (
        db.query(models.Team)
        .filter(models.Team.full_name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results


@router.get("/random", response_model=schemas.TeamResponse)
def get_random_team(db: Session = Depends(get_db)):

    results = db.query(models.Team).all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No teams found",
        )
    team = random.choice(results)
    return team


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_return = {}
    for field in FIELDS:
        team_return[field] = getattr(team, field)

    logo_urls = []

    for logo in LOGO_FIELDS:
        logo_url = getattr(team, logo)
        if not logo_url:
            logo_url = ""

        logo_urls.append({logo: logo_url})

    team_return["logo_urls"] = logo_urls

    record_appearances = {}
    for field in APP_FIELDS:
        app_field = getattr(team, field)
        record_appearances[field] = app_field

    team_return["record_appearances"] = record_appearances

    record_goals = {}
    for field in APP_FIELDS:
        goals_field = getattr(team, field)
        record_goals[field] = goals_field

    team_return["record_goals"] = record_goals

    return team_return


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_team(
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
def update_team(
    id: int,
    updated_team: schemas.TeamCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_query.update(updated_team.dict(), synchronize_session=False)
    db.commit()

    return team_query.first()
