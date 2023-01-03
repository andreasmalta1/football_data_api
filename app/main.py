from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from app.routers import auth, logo, request, team, user
except ImportError:
    from routers import auth, logo, request, team, user

app = FastAPI(
    title="Football Data Api",
    description="API for football data containibg teams in Europe's top 5 leagues and beyond, stadiums and competions and corresponding logos",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Andreas Calleja",
        "url": "",
        "email": "andreascalleja@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(logo.router)
app.include_router(request.router)
app.include_router(team.router)
app.include_router(user.router)

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

# 4. Add index home page - to add links to GitHub, LinkedIn, Docs, how to use
