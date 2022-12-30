from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

try:
    from app.database import get_db
    import app.schemas as schemas
    import app.models as models
    import app.utils as utils
except ImportError:
    from database import get_db
    import schemas
    import models
    import utils

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
    include_in_schema=False,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    results = db.query(models.User).all()
    if len(results) != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot create user",
        )

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
