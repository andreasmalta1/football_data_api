from passlib.context import CryptContext

try:
    import app.models as models
    from app.config import settings
except ImportError:
    import models
    from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def post_request(db, endpoint, request):
    new_request = models.Requests(
        endpoint=endpoint,
        method=request.method,
        path=request.get("path"),
        client_host=request.client.host,
        client_port=request.client.port,
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)


def get_team_return(team):
    FIELDS = [
        "id",
        "full_name",
        "name",
        "code",
        "nickname",
        "stadium",
        "competition",
        "website",
        "twitter_handle",
        "national_team",
        "year_formed",
        "country",
        "num_domestic_champions",
        "created_at",
    ]

    LOGO_FIELDS = ["logo_url_small", "logo_url_medium", "logo_url_large"]
    APP_FIELDS = ["player_record_appearances", "record_num_appearances"]
    GOAL_FIELDS = ["player_record_goals", "record_num_goals"]

    team_return = {}
    for field in FIELDS:
        team_return[field] = getattr(team, field)

        logo_urls = []

    for logo in LOGO_FIELDS:
        logo_url = getattr(team, logo)
        if not logo_url:
            logo_url = ""
        else:
            logo_url = settings.host_site + logo_url[2:]

        logo_urls.append({logo: logo_url})

    team_return["logo_urls"] = logo_urls

    record_appearances = {}
    for field in APP_FIELDS:
        app_field = getattr(team, field)
        if not app_field:
            app_field = ""
        record_appearances[field] = app_field

    team_return["record_appearances"] = record_appearances

    record_goals = {}
    for field in GOAL_FIELDS:
        goals_field = getattr(team, field)
        if not goals_field:
            goals_field = ""
        record_goals[field] = goals_field

    team_return["record_goals"] = record_goals

    return team_return
