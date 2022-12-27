from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from app.routers import team, logo, user
except ImportError as e:
    from routers import team, logo, user

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(team.router)
app.include_router(logo.router)
app.include_router(user.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Key -> https://testdriven.io/tips/6840e037-4b8f-4354-a9af-6863fb1c69eb/
# Only Admin can post

# New Tables for future
# Competetion
# Stadium


# https://www.akana.com/blog/what-is-api-monetization
