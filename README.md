# FastAPI Mini Backend

A production-structured REST API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.

This is my main portfolio project — built as part of my journey from Sales to Python Backend Developer. I am expanding it step by step, adding new features and patterns as I learn them.

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (python-jose) + bcrypt (passlib)
- **Testing:** pytest with isolated PostgreSQL test database
- **Architecture:** 3-layer (Presentation → Core → Infrastructure)

---

## Project Structure

```
fastapi-mini-backend/
├── app/
│   ├── main.py                  # App entry point, middleware, routers
│   ├── alembic/                 # Database migrations
│   ├── core/                    # Business logic layer
│   │   ├── authentication.py    # JWT + bcrypt
│   │   ├── enums.py             # UserRole, TodoStatus, TodoPriority
│   │   ├── security.py          # Role-based access control
│   │   ├── todo_service.py      # Todo business logic
│   │   └── user_service.py      # User business logic
│   ├── infrastructure/          # Database layer
│   │   ├── database.py          # SQLAlchemy engine + session
│   │   ├── models.py            # User + Todo ORM models
│   │   └── repositories/        # Database queries
│   │       ├── todo_repository.py
│   │       └── user_repository.py
│   ├── presentation/            # API layer
│   │   ├── schemas.py           # Pydantic request/response models
│   │   └── routers/             # FastAPI routers
│   │       ├── user_router.py   # Register, login
│   │       ├── todo_router.py   # Todo CRUD
│   │       ├── admin_router.py  # Admin endpoints
│   │       └── general_routes.py # /me endpoint
│   └── tests/                   # pytest test suite
│       ├── conftest.py
│       ├── test_user.py
│       ├── test_auth.py
│       ├── test_todo.py
│       └── test_admin.py
├── .env.example
├── alembic.ini
└── pytest.ini
```

---

## Features

- User registration and login with JWT authentication
- bcrypt password hashing
- Role-based access control (admin / user)
- Todo CRUD — create, read, update, soft delete
- Admin endpoints — hard delete, manage any user's todos
- Pagination on all list endpoints (limit / offset)
- GET /me — returns current logged-in user profile
- Custom middleware — request logging with response time
- CORS configured
- Full test suite — 31 tests, all passing

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /register | Register new user | No |
| POST | /login | Login, returns JWT token | No |
| GET | /me | Get current user profile | Yes |

### Todos
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /todos/create_todo | Create a todo | Yes |
| GET | /todos/get_all_todos | Get all your todos (paginated) | Yes |
| GET | /todos/get_todo_by_id/{id} | Get a single todo | Yes |
| PUT | /todos/update_todo/{id} | Update a todo | Yes |
| DELETE | /todos/delete_todo/{id} | Soft delete a todo | Yes |

### Admin
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /admin/ | Admin panel | Admin only |
| GET | /admin/get_all_todos/{user_id} | Get any user's todos (paginated) | Admin only |
| GET | /admin/get_todo_by_id/{id} | Get any todo | Admin only |
| PUT | /admin/update_todo/{id} | Update any todo | Admin only |
| DELETE | /admin/hard_delete_todo/{id} | Hard delete a todo | Admin only |
| DELETE | /admin/delete_user/{id} | Delete a user | Admin only |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/jandaghi14/fastapi-mini-backend.git
cd fastapi-mini-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your values:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/your_db_name
DATABASE_URL_TEST=postgresql://postgres:yourpassword@localhost:5432/your_test_db_name
SECRET_KEY=your-secret-key
```

### 5. Generate a secure SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

### 6. Run Alembic migrations
```bash
alembic upgrade head
```

### 7. Run the application
```bash
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

---

## Running Tests

Create a test database in PostgreSQL, then update `conftest.py` with your test database URL.

```bash
pytest -vv
```

Expected: **34 tests passing**

---

## Architecture

This project follows a 3-layer architecture:

```
Request → Presentation (routers) → Core (services) → Infrastructure (repositories) → Database
```

- **Routers** handle HTTP — request/response, status codes, schemas
- **Services** handle business logic — rules, validation, authorization
- **Repositories** handle database — queries only, no business logic

---

## Current Status

This project is actively being developed. Features being added next:

- [ ] Alembic migrations replacing create_all in tests
- [ ] Docker + docker-compose
- [ ] GitHub Actions CI/CD pipeline
- [ ] Railway deployment

---

## Author

Ali Jandaghi — Python Backend Developer

GitHub: [github.com/jandaghi14](https://github.com/jandaghi14)

LinkedIn: [ali-jandaghi-9a3188b1](https://www.linkedin.com/in/ali-jandaghi-9a3188b1)