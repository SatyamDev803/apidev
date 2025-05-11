# API Development with FastAPI and PostgreSQL

This project is a RESTful API built using **FastAPI** and **PostgreSQL**. It provides endpoints for managing posts, including creating, reading, updating, and deleting posts.

## Features

- **FastAPI** for building the API
- **PostgreSQL** as the database for storing data
- **SQLAlchemy** for ORM-based database interaction
- **Pydantic** for data validation and serialization
- Basic CRUD operations for posts
- Database connection pooling and error handling
- Interactive API documentation with Swagger UI
- Environment variables support for configuration
- Asynchronous database operations

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- A virtual environment (recommended)
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

4. **Configure the environment**:
   - Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://<username>:<password>@<host>/<database_name>
   ```

5. **Set up the PostgreSQL database**:
   - Create a database named `apidev`
   - Update the database credentials in your `.env` file
   - The application will handle table creation automatically

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure

```
apidev/
├── app/
│   ├── __init__.py      # Package initializer
│   ├── main.py          # Application entry point
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── crud/            # CRUD operations
├── tests/               # Unit and integration tests
├── .env                 # Environment variables
├── .gitignore          # Git ignore file
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## API Endpoints

| Method | Endpoint       | Description              | Status Codes    |
|--------|---------------|--------------------------|----------------|
| GET    | `/`           | Welcome message          | 200           |
| GET    | `/posts`      | Retrieve all posts       | 200           |
| POST   | `/posts`      | Create a new post        | 201, 400      |
| GET    | `/posts/{id}` | Retrieve a specific post | 200, 404      |
| PUT    | `/posts/{id}` | Update a specific post   | 200, 404      |
| DELETE | `/posts/{id}` | Delete a specific post   | 204, 404      |

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
```

## Error Handling

The API implements proper error handling for:
- Database connection errors
- Invalid request data
- Resource not found
- Authentication errors (if implemented)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request