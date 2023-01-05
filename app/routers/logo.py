from fastapi import (
    status,
    APIRouter,
    HTTPException,
    Request,
    Response,
    UploadFile,
    Depends,
    File,
)
from sqlalchemy.orm import Session
from PIL import Image, ImageOps
import os

try:
    from app.database import get_db
    from app.config import settings
    from app.utils import post_request, get_team_return
    import app.schemas as schemas
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    from config import settings
    from utils import post_request, get_team_return
    import schemas
    import models
    import oauth2


router = APIRouter(prefix="/api/logos", tags=["Logos"])

LOGO_FIELDS = ["logo_url_small", "logo_url_medium", "logo_url_large"]


@router.post(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.TeamResponse,
    include_in_schema=False,
)
async def create_logo(
    request: Request,
    id: int,
    file: UploadFile = File(...),
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

    logos_path = "./static/images/logos/"
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

        size = logo_types.get(logo).get("size")

        img = Image.open(logo_types.get(logo).get("path"))
        img = ImageOps.contain(img, (size, size))
        img.save(logo_types.get(logo).get("path"))

        setattr(
            team,
            logo_types.get(logo).get("field"),
            logo_types.get(logo).get("path"),
        )

    file.close()

    db.add(team)
    db.commit()
    db.refresh(team)

    team_return = get_team_return(team)

    post_request(db, "logos", request)

    return team_return


@router.get("/{id}", response_model=schemas.LogoResponse)
def get_logos(request: Request, id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    urls = []
    for logo in LOGO_FIELDS:
        logo_url = getattr(team, logo)
        if not logo_url:
            logo_url = ""
        else:
            logo_url = settings.host_site + logo_url[2:]

        urls.append({logo: logo_url})

    post_request(db, "logos", request)

    return {"logo_urls": urls}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_logo(
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

    post_request(db, "logos", request)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
