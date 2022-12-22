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


# TODO
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
# Figure out size for medium large and small images
