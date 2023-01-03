from fastapi import status, APIRouter, HTTPException, Response, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
import random

try:
    from app.database import get_db
    from app.utils import post_request
    import app.models as models
    import app.oauth2 as oauth2
except ImportError:
    from database import get_db
    from utils import post_request
    import models
    import oauth2


router = APIRouter(prefix="/api/requests", tags=["Teams"])


@router.get(
    "/",
    include_in_schema=False,
)
def get_requests(
    request: Request,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):

    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action",
        )

    request = post_request(db, "requests", request)

    results = db.query(models.Requests).filter(models.Requests.method == "GET").all()
    output = dict()
    for result in results:
        output[getattr(result, "endpoint")] = (
            output.get(getattr(result, "endpoint"), 0) + 1
        )

    return output
