from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
    import app.utils as utils
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    import schemas
    import models
    import utils
    import oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/api/login", response_model=schemas.Token, include_in_schema=False)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token["token"], "token_type": "bearer"}
