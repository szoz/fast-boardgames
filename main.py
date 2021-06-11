from fastapi import FastAPI

from routers import misc, items, users

app = FastAPI()
app.include_router(misc.router, tags=['miscellaneous'])
app.include_router(items.router)
app.include_router(users.router, tags=['authentication'])
