from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_db
import schemas
import models

router = APIRouter()


@router.get('/categories', response_model=List[schemas.Category], tags=['category'])
async def get_categories(db: Session = Depends(get_db)):
    """Redirects to Open API docs."""
    return db.query(models.Category).all()
