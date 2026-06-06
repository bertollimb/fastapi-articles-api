from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(
    title='Articles API',
    description='REST API with user authentication and article management, built with FastAPI, PostgreSQL, SQLAlchemy async and JWT.',
    version='1.0.0',
    contact={
        "name": "Matheus Bertolli",
        "url": "https://github.com/bertollimb",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "users", "description": "Operations related to user management and authentication."},
        {"name": "articles", "description": "Operations related to article management."},
    ]
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)
