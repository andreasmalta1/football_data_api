from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


try:
    from app.routers import auth, favicon, logo, request, team, user
    from app.backend.general_pages.route_homepage import general_pages_router
except ImportError:
    from routers import auth, favicon, logo, request, team, user
    from backend.general_pages.route_homepage import general_pages_router


tags_metadata = [
    {
        "name": "Teams",
        "description": "Operations with teams",
    },
    {
        "name": "Logos",
        "description": "Operations with logos",
    },
]


app = FastAPI(
    title="Football Data Api",
    description="API for football data containibg teams in Europe's top 5 leagues and beyond, stadiums and competions and corresponding logos",
    version="0.0.1",
    terms_of_service="",
    contact={
        "name": "Andreas Calleja",
        "email": "andreascalleja@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(favicon.router)
app.include_router(logo.router)
app.include_router(request.router)
app.include_router(team.router)
app.include_router(user.router)
app.include_router(general_pages_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
