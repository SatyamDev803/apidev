# Full Stack Social Media Platform with FastAPI and Next.js

This project is a full-stack social media platform built using **FastAPI** for the backend API and **Next.js** for the frontend. It provides a modern, scalable architecture for managing posts, users, authentication, and interactive features.

## Technology Stack

### Backend
- **FastAPI**: High-performance web framework for building APIs
- **PostgreSQL**: Robust, open-source database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Alembic**: Database migration tool
- **JWT**: JSON Web Token for authentication
- **OAuth2**: Industry-standard protocol for authorization

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Static typing for JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **Axios**: HTTP client for API requests

### DevOps & Deployment
- **Docker**: Containerization
- **Nginx**: High-performance web server
- **Gunicorn**: Python WSGI HTTP Server
- **Render**: Cloud hosting platform

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

### Backend Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip package manager
- Docker (optional, for containerization)

### Frontend Requirements
- Node.js 18 or higher
- npm or yarn package manager
- Git

### Development Tools
- VS Code (recommended) with extensions:
  - Python
  - Pylance
  - ESLint
  - Prettier
  - Docker
  - GitLens

## Setup Instructions

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd apidev
   ```

2. **Create and activate virtual environment**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install backend dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Create frontend environment file**:
   Create a `.env.local` file in the frontend directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
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
├── alembic/                # Database migrations
│   └── versions/           # Migration versions
├── app/                    # Backend application
│   ├── routers/           # API routes
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── post.py        # Post operations
│   │   ├── user.py        # User operations
│   │   └── vote.py        # Voting system
│   ├── __init__.py     
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup & connection
│   ├── main.py           # App entry point
│   ├── models.py          # SQLAlchemy models
│   ├── oauth2.py          # Authentication logic
│   ├── schemas.py         # Pydantic models
│   └── utils.py           # Utility functions
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Next.js 14 app directory
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── posts/    # Post-related pages
│   │   │   └── auth/     # Authentication pages
│   │   ├── components/   # Reusable components
│   │   ├── lib/         # Utility functions
│   │   └── types/       # TypeScript types
│   ├── public/          # Static assets
│   └── package.json     # Frontend dependencies
├── tests/                 # Test suite
├── docker-compose-dev.yml # Docker development config
├── docker-compose-prod.yml # Docker production config
├── Dockerfile             # Backend Docker build
├── frontend.Dockerfile    # Frontend Docker build
├── gunicorn.service      # Systemd service
├── nginx/                # Nginx configuration
└── render.yaml           # Render deployment config
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

### Running the Application

1. **Start the Backend**:
   ```bash
   # Development mode
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Production mode
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

2. **Start the Frontend**:
   ```bash
   # Development mode
   cd frontend
   npm run dev
   # or
   yarn dev

   # Production build
   npm run build
   npm start
   ```

### Running Tests

1. **Backend Tests**:
   ```bash
   # Run all tests
   pytest

   # Run specific test file
   pytest tests/test_users.py -v

   # Run with output
   pytest -v -s

   # Run with coverage
   pytest --cov=app tests/
   ```

2. **Frontend Tests**:
   ```bash
   cd frontend
   npm test
   # or
   yarn test
   ```

### Docker Development

1. **Development Environment**:
   ```bash
   # Start all services
   docker-compose -f docker-compose-dev.yml up -d

   # View logs
   docker-compose -f docker-compose-dev.yml logs -f

   # Stop services
   docker-compose -f docker-compose-dev.yml down
   ```

2. **Production Environment**:
   ```bash
   # Start all services
   docker-compose -f docker-compose-prod.yml up -d

   # View logs
   docker-compose -f docker-compose-prod.yml logs -f

   # Stop services
   docker-compose -f docker-compose-prod.yml down
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

## Error Handling and Security

### Backend Error Handling
- Authentication/Authorization errors
- Database connection issues
- Resource not found errors
- Input validation errors
- Duplicate entry handling
- Foreign key violations
- Rate limiting
- CORS configuration
- Request validation
- Response validation

### Frontend Error Handling
- API error handling
- Form validation
- Loading states
- Error boundaries
- Authentication state management
- Network error handling
- Optimistic updates
- Toast notifications

### Security Features
- Password hashing with bcrypt
- JWT token authentication
- HTTPS enforcement
- SQL injection prevention
- XSS protection
- CSRF protection
- Rate limiting
- Input sanitization
- Secure headers
- Cookie security

## Deployment

### Backend Deployment
1. **Docker Containerization**:
   - Multi-stage builds
   - Environment-specific configurations
   - Volume management
   - Container health checks

2. **Nginx Configuration**:
   - Reverse proxy setup
   - SSL/TLS configuration
   - Caching strategies
   - Load balancing
   - Static file serving

3. **Gunicorn Setup**:
   - Worker configuration
   - Performance tuning
   - Logging setup
   - Process management

### Frontend Deployment
1. **Static Site Generation**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Production Optimization**:
   - Code splitting
   - Image optimization
   - Font optimization
   - Cache management
   - Performance monitoring

### Cloud Deployment
The project is configured for deployment on Render.com:
- Automatic deployments
- Environment variables management
- SSL certificates
- Custom domains
- Database management
- Continuous monitoring

## Performance Optimization

### Backend Optimization
- Database indexing
- Query optimization
- Connection pooling
- Caching strategies
- Async operations
- Resource compression
- Memory management
- Batch processing

### Frontend Optimization
- Code splitting
- Lazy loading
- Image optimization
- Cache management
- Bundle size optimization
- Tree shaking
- Memory leaks prevention
- Performance monitoring

## Contributing

1. **Fork the Repository**:
   - Click the Fork button on GitHub
   - Clone your fork locally

2. **Set Up Development Environment**:
   ```bash
   # Clone repository
   git clone <your-fork-url>
   cd apidev

   # Create branch
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**:
   - Follow coding standards
   - Add tests for new features
   - Update documentation
   - Ensure all tests pass

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Contact the maintainers
- Join our community discussions

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.