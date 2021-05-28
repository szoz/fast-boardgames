from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from pydantic import PositiveInt

from dependencies import get_db
import schemas
import models

router = APIRouter()


@router.get('/categories', response_model=List[schemas.Category], tags=['category'])
async def get_categories(db: Session = Depends(get_db)):
    """Return list of all categories."""
    return db.query(models.Category).all()


@router.get('/boardgames', response_model=List[schemas.Boardgame], tags=['boardgames'])
async def get_boardgames(response: Response, db: Session = Depends(get_db),
                         limit: PositiveInt = 20, page: PositiveInt = 1):
    """Return list of all boardgames with given sorting and pagination params."""
    response.headers['X-Total-Count'] = str(db.query(models.Boardgames).count())
    offset = limit * (page - 1)

    records = db.query(models.Boardgames) \
        .limit(limit).offset(offset).all()

    return records
