from fastapi import status, APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import create_model
import random

try:
    from app.database import get_db
    from app.utils import post_request, get_team_return
    import app.schemas as schemas
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    from utils import post_request, get_team_return
    import schemas
    import models
    import oauth2


router = APIRouter(prefix="/api/teams", tags=["Teams"])

query_params = {
    "name": (str, None),
    "code": (str, None),
    "nickname": (str, None),
    "stadium": (str, None),
    "competition": (str, None),
    "country": (str, None),
    "location": (str, None),
    "national": (bool, None),
}

query_model = create_model("Query", **query_params)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TeamResponse,
    include_in_schema=False,
)
def create_team(
    request: Request,
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

    post_request(db, "teams", request)

    return new_team


@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    params: query_model = Depends(),
):

    params_dict = params.dict()
    results = db.query(models.Team)

    for key in params_dict:
        if key == "national" and params_dict[key] is not None:
            results = results.filter(
                models.Team.national_team == params_dict["national"]
            )
            continue

        if params_dict[key]:

            results = results.filter(
                func.lower(getattr(models.Team, key)).contains(params_dict[key].lower())
            )
    results = results.order_by(models.Team.id).limit(limit).offset(skip).all()

    return_results = [get_team_return(team) for team in results]

    post_request(db, "teams", request)

    return return_results


@router.get("/random", response_model=schemas.TeamResponse)
def get_random_team(
    request: Request,
    db: Session = Depends(get_db),
    params: query_model = Depends(),
):

    params_dict = params.dict()
    results = db.query(models.Team)

    for key in params_dict:
        if key == "national" and params_dict[key] is not None:
            results = results.filter(
                models.Team.national_team == params_dict["national"]
            )
            continue

        if params_dict[key]:
            results = results.filter(
                func.lower(getattr(models.Team, key)).contains(params_dict[key].lower())
            )

    results = results.all()

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No teams found",
        )
    team = random.choice(results)
    team_return = get_team_return(team)

    post_request(db, "teams", request)

    return team_return


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, request: Request, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    team_return = get_team_return(team)
    post_request(db, "teams", request)

    return team_return


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_team(
    request: Request,
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

    post_request(db, "teams", request)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.TeamResponse, include_in_schema=False)
def update_team(
    request: Request,
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

    post_request(db, "teams", request)

    return team_query.first()
