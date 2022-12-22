from fastapi import FastAPI, File, UploadFile, status, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from PIL import Image
import secrets

try:
    from app.database import get_db
    import app.models as models
    import app.schemas as schemas
except ImportError:
    from database import get_db
    import models
    import schemas

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"data": "home"}


@app.post("/", status_code=status.HTTP_201_CREATED)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
):

    new_team = models.Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@app.get("/{id}")
def get_team(id: int, db: Session = Depends(get_db)):
    team = db.query(models.Team).filter(models.Team.id == id).first()

    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )
    return team


@app.post("/uploadlogos/{id}", status_code=status.HTTP_201_CREATED)
async def create_file(
    id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):

    team_query = db.query(models.Team).filter(models.Team.id == id)
    team = team_query.first()

    if team == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {id} was not found",
        )

    FILEPATH = "./static/images"
    filename = file.filename
    extension = filename.split(".")[1]
    if extension not in ["jpg"]:
        return {"status": "error"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    # Resize
    # img = Image.open(generated_name)
    # img = img.resize(size=(200, 200))
    # img.save(generated_name)

    file.close()
    setattr(team, "url", generated_name)

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


# Updating logo
# Change name
# Change location
# Add host
# Return statement

# Id invalid for logo
# Return models
# Make url can be null
# Ensure using all protocols i.e. schemas, repsonses ...
# Start routing
# Build table/tables
