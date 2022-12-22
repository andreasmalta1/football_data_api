from fastapi import (
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    File,
    UploadFile,
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
    if extension != "jpg":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Logo format must be .jpg",
        )

    team_name = getattr(team, "name").lower().replace(" ", "_")
    logo_file_name = f"{logos_path}{team_name}-{id}.{extension}"
    file_content = await file.read()

    with open(logo_file_name, "wb") as file:
        file.write(file_content)

    # Resize
    # img = Image.open(generated_name)
    # img = img.resize(size=(200, 200))
    # img.save(generated_name)

    file.close()
    setattr(team, "url", logo_file_name)

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


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
            detail=f"Post with id {id} was not found",
        )

    logo_name = getattr(team, "url")
    print(logo_name)
    os.remove(logo_name)
    setattr(team, "url", None)

    db.add(team)
    db.commit()
    db.refresh(team)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
