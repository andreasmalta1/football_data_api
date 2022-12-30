from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from app.routers import team, logo, user, auth
except ImportError as e:
    from routers import team, logo, user, auth

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(team.router)
app.include_router(logo.router)
app.include_router(user.router)
app.include_router(auth.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# New Tables for future
# Competition
# Stadium

# https://www.akana.com/blog/what-is-api-monetization
# https://www.linkedin.com/pulse/9-ways-promote-your-api-gj-de-wilde-we-re-hiring-/


# 1. Add host name in .env to add it to static files
# 2. Get number of requests made: https://fastapi.tiangolo.com/advanced/using-request-directly/
# 3. Check images folder. Keep in mind that new image structure will be added for stadia
# 4. Add index home page - to add links to GitHub, LinkedIn, Docs, how to use
