from fastapi import FastAPI

from routers import misc, items, users

tags_metadata = [
    {'name': 'miscellaneous'},
    {'name': 'categories', 'description': 'Boardgames categories details'},
    {'name': 'boardgames', 'description': 'Boardgames details'},
    {'name': 'authentication', 'description': 'Logging in and managing session'},
    {'name': 'users', 'description': 'Users details'}
]

app = FastAPI(title='Fast Boardgames', version='0.2', openapi_tags=tags_metadata,
              description='REST API with information about best 100 boardgames.')

app.include_router(misc.router, tags=['miscellaneous'])
app.include_router(items.router)
app.include_router(users.router)
