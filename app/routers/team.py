from fastapi import status, APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
except ImportError:
    from database import get_db
    import schemas
    import models


router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamResponse
)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
):
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


@router.get("/{id}", response_model=schemas.TeamResponse)
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )
    return team


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    id: int,
    db: Session = Depends(get_db),
):
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


@router.put("/{id}", response_model=schemas.TeamResponse)
def update_team(
    id: int, updated_team: schemas.TeamCreate, db: Session = Depends(get_db)
):
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
