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
        "description": "You can get teams with information including name, nickname, stadium, competition, country, location, logos, website, year formed and player records",
    },
    {
        "name": "Logos",
        "description": "Get request for team logos returning 3 urls for a small, medium and large sized logo",
    },
]

description = """
TheFootballData API ⚽ provides data for Europe's top 5 football leagues and beyond, including information on teams, competitions, nations, and stadiums. It also includes logos for each entity. The API is constantly updated with new data. If any data is missing or incorrect, contact me on andreascalleja@gmail.com have it fixed. 💻
<br></br>
Please see each get request for more information including query parameters
"""


app = FastAPI(
    title="Football Data Api",
    description=description,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    version="1.0.0",
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
