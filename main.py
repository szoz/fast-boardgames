from fastapi import FastAPI

from routers import misc, items

app = FastAPI()
app.include_router(misc.router, tags=['miscellaneous'])
app.include_router(items.router)
