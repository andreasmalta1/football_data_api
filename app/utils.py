from passlib.context import CryptContext

try:
    import app.models as models
except ImportError:
    import models

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
