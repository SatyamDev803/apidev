# API Development with FastAPI and PostgreSQL

This project is a RESTful API built using **FastAPI** and **PostgreSQL**. It provides endpoints for managing posts, users, votes, and authentication.

## Features

- **FastAPI** for building high-performance REST APIs
- **PostgreSQL** as the database backend
- **SQLAlchemy** for ORM-based database operations
- **Pydantic** for data validation and serialization
- **Alembic** for database migrations
- **JWT** based authentication
- **OAuth2** with Password flow
- **Docker** support for containerization
- **Nginx** for reverse proxy
- **Gunicorn** for production deployment
- Full CRUD operations for posts and users
- Voting system for posts
- Database connection pooling
- Error handling and logging
- Interactive API documentation (Swagger UI)
- Environment-based configuration
- Comprehensive test suite
- CI/CD ready with render.yaml

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- Docker (optional, for containerization)
- pip package manager

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd apidev
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file with:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_PASSWORD=your_password
   DATABASE_NAME=apidev
   DATABASE_USERNAME=postgres
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Database Setup**:
   ```bash
   # Create main and test databases
   createdb apidev
   createdb apidev_test

   # Run migrations
   alembic upgrade head
   ```

6. **Run the application**:
   ```bash
   # Development
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Production
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

## Project Structure

```
apidev/
├── alembic/              # Database migrations
│   └── versions/         # Migration versions
├── app/                  # Main application
│   ├── routers/         # API routes
│   │   ├── auth.py     # Authentication
│   │   ├── post.py     # Post operations
│   │   ├── user.py     # User operations
│   │   └── vote.py     # Voting system
│   ├── __init__.py     
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── main.py         # App entry point
│   ├── models.py        # SQLAlchemy models
│   ├── oauth2.py        # Authentication
│   ├── schemas.py       # Pydantic models
│   └── utils.py         # Utilities
├── tests/               # Test suite
├── docker-compose-dev.yml   # Docker dev config
├── docker-compose-prod.yml  # Docker prod config
├── Dockerfile           # Docker build
├── gunicorn.service    # Systemd service
├── nginx/              # Nginx config
└── render.yaml         # Render deployment
```

## API Endpoints

| Method | Endpoint          | Description              | Auth Required |
|--------|------------------|--------------------------|--------------|
| POST   | `/users/`        | Create user              | No           |
| GET    | `/users/{id}`    | Get user                 | No           |
| POST   | `/login`         | Login user               | No           |
| GET    | `/posts`         | Get all posts            | Yes          |
| POST   | `/posts`         | Create post              | Yes          |
| GET    | `/posts/{id}`    | Get post                 | Yes          |
| PUT    | `/posts/{id}`    | Update post              | Yes          |
| DELETE | `/posts/{id}`    | Delete post              | Yes          |
| POST   | `/vote`          | Vote on post             | Yes          |

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py -v

# Run with output
pytest -v -s
```

### Docker Development
```bash
# Development environment
docker-compose -f docker-compose-dev.yml up -d

# Production environment
docker-compose -f docker-compose-prod.yml up -d
```

### Database Migrations
```bash
# Create new migration
alembic revision -m "description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Error Handling

The API implements comprehensive error handling for:
- Authentication/Authorization errors
- Database connection issues
- Resource not found
- Validation errors
- Duplicate entries
- Foreign key violations

## Deployment

The project includes configuration for:
- Docker containerization
- Nginx as reverse proxy
- Gunicorn as WSGI server
- Render.com deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.