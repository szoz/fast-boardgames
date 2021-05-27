from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get('/')
async def get_index():
    """Redirects to Open API docs."""
    return RedirectResponse('/docs')
