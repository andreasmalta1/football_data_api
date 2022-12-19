from fastapi import FastAPI, File, UploadFile, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from PIL import Image
import io
import secrets

try:
    from app.database import get_db
    import app.models as models
except ImportError:
    from database import get_db
    import models

app = FastAPI()

app.mount("/static", StaticFiles(directroy="static", name="static"))

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


@app.post("/files", status_code=status.HTTP_201_CREATED)
# async def create_file(file: bytes = File(...), db: Session = Depends(get_db)):
async def create_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    FILEPATH = "./static/images"
    filename = file.filename
    extension = filename.split(".")[1]
    if extension not in ["jpg"]:
        return {"status": "error"}
    # image = Image.open(io.BytesIO(file))
    # image.show()
    # new_post = models.Post(img=image, name="AA", mimetype="jpeg")
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
