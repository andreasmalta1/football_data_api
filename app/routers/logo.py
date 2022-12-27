from fastapi import (
    status,
    APIRouter,
    HTTPException,
    Response,
    UploadFile,
    Depends,
    File,
)
from sqlalchemy.orm import Session
from PIL import Image
import os

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
except ImportError:
    from database import get_db
    import schemas
    import models


router = APIRouter(prefix="/logos", tags=["Logos"])


@router.post(
    "/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamResponse
)
async def create_logo(
    id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    logos_path = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]
    if extension not in ["jpg", "png", "svg"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Logo format must be .jpg",
        )

    team_name = getattr(team, "name").lower().replace(" ", "_")
    file_content = await file.read()

    logo_types = {
        "logo_file_name_small": {
            "path": f"{logos_path}small/{team_name}-{id}.{extension}",
            "size": 200,
            "field": "logo_url_small",
        },
        "logo_file_name_medium": {
            "path": f"{logos_path}medium/{team_name}-{id}.{extension}",
            "size": 600,
            "field": "logo_url_medium",
        },
        "logo_file_name_large": {
            "path": f"{logos_path}large/{team_name}-{id}.{extension}",
            "size": 1200,
            "field": "logo_url_large",
        },
    }

    for logo in logo_types:
        with open(logo_types.get(logo).get("path"), "wb") as file:
            file.write(file_content)

        img = Image.open(logo_types.get(logo).get("path"))
        img = img.resize(
            size=(logo_types.get(logo).get("size"), logo_types.get(logo).get("size"))
        )
        img.save(logo_types.get(logo).get("path"))

        setattr(
            team,
            logo_types.get(logo).get("field"),
            logo_types.get(logo).get("path"),
        )
        print(logo_types.get(logo).get("field"))
        print(logo_types.get(logo).get("path"))

    file.close()

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


@router.get("/{id}", response_model=schemas.LogoResponse)
def get_logos(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()
    urls = [
        {"logo_url_small": getattr(team, "logo_url_small")},
        {"logo_url_medium": getattr(team, "logo_url_medium")},
        {"logo_url_large": getattr(team, "logo_url_large")},
    ]

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )
    return {"logo_urls": urls}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_logo(
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

    logo_urls = ["logo_url_small", "logo_url_medium", "logo_url_large"]
    for url in logo_urls:
        logo = getattr(team, url)
        if not logo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Logo for team with id {id} was not found",
            )

        os.remove(logo)
        setattr(team, url, None)

    db.add(team)
    db.commit()
    db.refresh(team)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
