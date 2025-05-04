# API Development with FastAPI and PostgreSQL

This project is a RESTful API built using **FastAPI** and **PostgreSQL**. It provides endpoints for managing posts, including creating, reading, updating, and deleting posts.

## Features

- **FastAPI** for building the API.
- **PostgreSQL** as the database for storing data.
- **Psycopg2** for database interaction.
- Basic CRUD operations for posts.
- Database connection pooling and error handling.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- A virtual environment (recommended)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd apidev
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database**:
   - Create a database named `apidev`.
   - Update the database credentials in `main.py`:
     ```python
     conn = psycopg2.connect(
         host='localhost',
         database='apidev',
         user='postgres',
         password='rootuser',
         cursor_factory=RealDictCursor
     )
     ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API documentation**:
   - Open your browser and navigate to `http://127.0.0.1:8000/docs` for the Swagger UI.

## Project Structure

```
apidev/
├── app/
│   ├── main.py          # Main application file
│   ├── __init__.py      # Marks the app directory as a package
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
```

## Endpoints

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| GET    | `/`            | Welcome message         |
| GET    | `/posts`       | Retrieve all posts      |
| POST   | `/posts`       | Create a new post       |
| GET    | `/posts/{id}`  | Retrieve a specific post|
| DELETE | `/posts/{id}`  | Delete a specific post  |
| PUT    | `/posts/{id}`  | Update a specific post  |

## Environment Variables

- Create a `.env` file to store sensitive information like database credentials.

## License

This project is licensed under the MIT License.