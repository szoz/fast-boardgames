from fastapi import APIRouter, Depends, Response, Path, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List
from pydantic import PositiveInt

from dependencies import get_db
import schemas
import models

router = APIRouter()


@router.get('/categories', response_model=List[schemas.Category], tags=['categories'])
async def get_categories(db: Session = Depends(get_db)):
    """Return list of all categories."""
    return db.query(models.Categories).all()


@router.get('/boardgames', response_model=List[schemas.Boardgame], tags=['boardgames'])
async def get_boardgames(response: Response, db: Session = Depends(get_db),
                         limit: PositiveInt = 20, page: PositiveInt = 1,
                         category: str = None, complexity: schemas.BoardgameComplexityEnum = None,
                         sort: schemas.BoardgameSortEnum = schemas.BoardgameSortEnum.score_):
    """Return list of all boardgames with given sorting and pagination params."""
    response.headers['X-Total-Count'] = str(db.query(models.Boardgames).count())

    offset = limit * (page - 1)
    order = desc(f"boardgames_{sort.lstrip('-')}") if sort.value.startswith('-') else f"boardgames_{sort}"
    order_secondary = desc('boardgames_id') if sort.value.startswith('-') else 'boardgames_id'

    base_query = db.query(models.Boardgames)

    if category:
        base_query = base_query.join(models.Boardgames.categories) \
            .filter(models.Categories.name.ilike(category))

    if complexity:
        base_query = base_query.filter(complexity.minimum <= models.Boardgames.complexity) \
            .filter(models.Boardgames.complexity < complexity.maximum)

    records = base_query.order_by(order, order_secondary) \
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
