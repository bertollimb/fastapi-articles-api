import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from core.database import Base
from core.deps import get_session

# in-memory database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine_test
)

# Replaces the real session with the test session.
async def override_get_session():
    async with SessionTest() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def user_data():
    return {
        "name": "Bruna",
        "lastname": "Bertolli",
        "email": "bruna@test.com",
        "password": "test4321",
        "is_admin": False,
    }

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
    

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def created_user(client, user_data):
    response = await client.post("/api/v1/users/signup", json=user_data)

    assert response.status_code == 201

    return {
        "request": user_data,
        "response": response.json()
    }

@pytest.fixture
async def auth_token(client, created_user):
    response = await client.post("/api/v1/users/login", data={
            "username": created_user["request"]["email"],
            "password": created_user["request"]["password"],
        },
    )

    return response.json()["access_token"]

@pytest.fixture
async def created_article(client, auth_token):
    response = await client.post(
        "/api/v1/articles/",
        json={
            "title": "An article",
            "description": "Just an article",
            "source_url": "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview",
        },
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )

    assert response.status_code == 201

    return response.json()
