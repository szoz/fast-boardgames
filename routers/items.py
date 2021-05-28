from fastapi import APIRouter, Depends, Response, Path, HTTPException
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


@router.get('/boardgames/{id}', response_model=schemas.Boardgame, responses={404: {'description': 'Not Found'}},
            tags=['boardgames'])
async def get_boardgame(boardgame_id: PositiveInt = Path(..., alias='id'), db: Session = Depends(get_db)):
    """Return boardgame based on given id."""
    record = db.query(models.Boardgames).get(boardgame_id)

    if not record:
        raise HTTPException(status_code=404, detail='record with given id not found')

    return record
