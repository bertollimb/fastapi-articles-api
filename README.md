# fastapi-articles-api

REST API with user authentication and article management, built with FastAPI, PostgreSQL, SQLAlchemy async and JWT.

This project simulates the backend of a multi-user publishing platform, where authenticated users can create, manage, and share articles. It was built to apply production-level backend practices such as layered architecture, secure authentication, asynchronous database operations, schema migrations, and automated integration testing.

---

## Technologies

- **Python 3.13**
- **FastAPI** — web framework
- **PostgreSQL** — relational database
- **SQLAlchemy 2.0** — async ORM
- **Alembic** — database migrations
- **asyncpg** — async PostgreSQL driver
- **Pydantic v2** — data validation and serialization
- **python-jose** — JWT token generation and validation
- **passlib + bcrypt** — password hashing
- **uvicorn** — ASGI server
- **pytest** — testing framework
- **pytest-asyncio** — async test support
- **httpx** — async API client for integration tests
- **SQLite** — isolated database for automated tests

---

## Project Structure

```text
fastapi-articles-api/
├── alembic/
│   ├── versions/
│   └── env.py
├── api/
│   └── v1/
│       ├── api.py
│       └── endpoints/
│           ├── article.py
│           └── user.py
├── core/
│   ├── auth.py
│   ├── configs.py
│   ├── database.py
│   ├── deps.py
│   └── security.py
├── models/
│   ├── __all_models.py
│   ├── article_model.py
│   └── user_model.py
├── schemas/
│   ├── article_schema.py
│   └── user_schema.py
├── tests/
│   ├── conftest.py
│   ├── test_articles.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── alembic.ini
├── create_tables.py
├── main.py
├── requirements.txt
└── LICENSE
```

---

## Features

- User registration and authentication with JWT
- Password hashing with bcrypt
- Protected routes via OAuth2
- Full CRUD for users and articles
- Async database sessions with SQLAlchemy and asyncpg
- Data validation with Pydantic v2
- Database schema versioning with Alembic
- Automated integration tests with pytest
- Isolated SQLite test database
- Reusable pytest fixtures for authentication and test data

---

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/bertollimb/fastapi-articles-api.git
cd fastapi-articles-api
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install fastapi psycopg2-binary sqlalchemy asyncpg uvicorn python-jose[cryptography] pytz passlib python-multipart pydantic-settings alembic bcrypt==4.0.1 "pydantic[email]" pytest pytest-asyncio httpx aiosqlite

pip freeze > requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DB_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
JWT_SECRET=yoursecrettoken
```

To generate a secure `JWT_SECRET`:

```python
import secrets

secrets.token_urlsafe(32)
```

**5. Apply database migrations**

```bash
alembic upgrade head
```

This creates all tables defined in `models/` using the migration history tracked in `alembic/versions/`.

**6. Run the server**

```bash
python main.py
```

The API will be available at:

```
http://localhost:8000
```

---

## Database Migrations

This project uses **Alembic** to manage database schema changes. The connection URL is injected automatically from `Settings.DB_URL` in `alembic/env.py`, so `alembic.ini` doesn't need to store credentials.

### Common commands

| Command | Description |
|---------|-------------|
| `alembic revision --autogenerate -m "message"` | Generate a new migration based on model changes |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Revert the last migration |
| `alembic history` | List migration history |
| `alembic current` | Show the current migration applied to the database |

### Adding a new model

1. Create the model in `models/` inheriting from `Base` (`core/database.py`).
2. Import the model in `alembic/env.py`.
3. Run:

```bash
alembic revision --autogenerate -m "create <table> table"
```

4. Review the generated migration.
5. Apply it:

```bash
alembic upgrade head
```

---

## Testing

The project includes automated integration tests covering authentication and article management.

### Test Stack

- **pytest** for test execution
- **pytest-asyncio** for asynchronous tests
- **httpx.AsyncClient** for HTTP integration testing
- **SQLite** as an isolated test database

### Test Fixtures

Reusable fixtures defined in `tests/conftest.py` prepare the environment for each test and eliminate duplicated setup code.

| Fixture | Purpose |
|---------|---------|
| `client` | Creates an asynchronous HTTP client |
| `user_data` | Default payload used to create users |
| `created_user` | Creates a user for the current test |
| `auth_token` | Authenticates the created user and returns a JWT token |
| `article_data` | Default payload used to create articles |
| `created_article` | Creates an article associated with the authenticated user |

### Test Isolation

Each test runs against a fresh SQLite database.

The database schema is recreated before every test, ensuring:

- Tests are completely independent.
- Tests can run in any order.
- Tests do not share state.
- No test depends on another to execute successfully.

This approach follows common backend testing practices used in production environments.

### Running the tests

Run the entire test suite:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_users.py -v
```

```bash
pytest tests/test_articles.py -v
```

Run a single test:

```bash
pytest tests/test_articles.py::test_create_article -v
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the server, access:

| Interface | URL | Description |
|-----------|-----|-------------|
| Swagger UI | `http://localhost:8000/docs` | Interactive documentation with request execution |
| ReDoc | `http://localhost:8000/redoc` | Read-only API documentation |

---

## API Endpoints

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/users/signup` | Register a new user | No |
| POST | `/api/v1/users/login` | Authenticate and receive a JWT token | No |
| GET | `/api/v1/users/logged` | Retrieve the authenticated user | Yes |
| GET | `/api/v1/users/` | List all users | Yes |
| GET | `/api/v1/users/{user_id}` | Retrieve a user with associated articles | Yes |
| PUT | `/api/v1/users/{user_id}` | Update a user | Yes |
| DELETE | `/api/v1/users/{user_id}` | Delete a user | Yes |

### Articles

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/articles/` | Create an article | Yes |
| GET | `/api/v1/articles/` | List all articles | No |
| GET | `/api/v1/articles/{article_id}` | Retrieve an article by ID | No |
| PUT | `/api/v1/articles/{article_id}` | Update an article | Yes |
| DELETE | `/api/v1/articles/{article_id}` | Delete an article | Yes |

---

## Authentication

The API uses **JWT Bearer Authentication**.

Workflow:

1. Register a user:

```
POST /api/v1/users/signup
```

2. Authenticate:

```
POST /api/v1/users/login
```

using the form fields:

- `username`
- `password`

3. Include the returned JWT in protected requests:

```http
Authorization: Bearer <access_token>
```

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.