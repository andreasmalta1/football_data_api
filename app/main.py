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


# Add response dictionairy of url
# Test new functionality esp for logos (delete/update)
# Resize images and different files for each size


# For schema of team respones, adjust dict in get function
