# fastapi-articles-api

REST API with user authentication and article management, built with FastAPI, PostgreSQL, SQLAlchemy async and JWT.

This project simulates the backend of a multi-user publishing platform, where authenticated users can create, manage, and share articles. It was built to apply production-level backend practices: layered architecture, secure authentication, async database operations, and fully documented endpoints.

---

## Technologies

- **Python 3.13**
- **FastAPI** — web framework
- **PostgreSQL** — relational database
- **SQLAlchemy 2.0** — async ORM
- **asyncpg** — async PostgreSQL driver
- **Pydantic v2** — data validation and serialization
- **python-jose** — JWT token generation and validation
- **passlib + bcrypt** — password hashing
- **uvicorn** — ASGI server

---

## Project Structure

```
fastapi-articles-api/
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
├── .env.example
├── .gitignore
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
pip install 
fastapi
psycopg2-binary
sqlalchemy
asyncpg
uvicorn
python-jose[cryptography]
pytz
passlib
python-multipart
pydantic-settings
bcrypt == 4.0.1 'pydantic[email]'

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

**5. Create the database tables**

```bash
python create_tables.py
```

**6. Run the server**

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

---

## API Documentation

FastAPI generates interactive documentation automatically. After running the server, access:

| Interface | URL | Description |
|-----------|-----|-------------|
| Swagger UI | `http://localhost:8000/docs` | Interactive — test endpoints directly in the browser |
| ReDoc | `http://localhost:8000/redoc` | Clean read-only documentation |

---

## API Endpoints

### Users

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/users/signup` | Register a new user | No |
| POST | `/api/v1/users/login` | Authenticate and get token | No |
| GET | `/api/v1/users/logged` | Get current logged user | Yes |
| GET | `/api/v1/users/` | List all users | Yes |
| GET | `/api/v1/users/{user_id}` | Get user by ID with articles | Yes |
| PUT | `/api/v1/users/{user_id}` | Update user | Yes |
| DELETE | `/api/v1/users/{user_id}` | Delete user | Yes |

### Articles

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/articles/` | Create a new article | Yes |
| GET | `/api/v1/articles/` | List all articles | No |
| GET | `/api/v1/articles/{article_id}` | Get article by ID | No |
| PUT | `/api/v1/articles/{article_id}` | Update article | Yes |
| DELETE | `/api/v1/articles/{article_id}` | Delete article | Yes |

---

## Authentication

This API uses **JWT Bearer Token** authentication.

1. Register a user via `POST /api/v1/users/signup`
2. Login via `POST /api/v1/users/login` using form fields `username` and `password`
3. Use the returned `access_token` in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_token>
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.