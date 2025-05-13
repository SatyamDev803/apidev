from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database URL format: 'postgresql://<username>:<password>@<host>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Create the SQLAlchemy engine
test_engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

