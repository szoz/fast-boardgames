from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.orm import Session

from dependencies import get_db
from auth import security_login, create_token
import models

router = APIRouter()


@router.get('/login', responses={401: {'description': 'Unauthorised'}}, tags=['authentication'])
async def login(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security_login)):
    """Redirects to Open API docs."""
    record = db.query(models.Users).filter_by(name=credentials.username).first()

    if not record or record.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return {'token': create_token(user=credentials.username)}


@router.get('/refresh-token', tags=['authentication'], deprecated=True)
async def refresh_token():
    ...


@router.get('/users', tags=['users'], deprecated=True)
async def get_users():
    ...


@router.get('/users/me', tags=['users'], deprecated=True)
async def get_user_me():
    ...
