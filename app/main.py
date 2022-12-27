from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from app.routers import team, logo
except ImportError as e:
    from routers import team, logo

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(team.router)
app.include_router(logo.router)

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


# Build table/tables
# Figure out size for medium large and small images
# Additional functionality??


# Resize images and different files for each size
# Logos in different folders according to size


# Test new functionality esp for logos (delete/update)

# API Key -> https://testdriven.io/tips/6840e037-4b8f-4354-a9af-6863fb1c69eb/
# Onky Admin can post
