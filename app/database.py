from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database URL format: 'postgresql://<username>:<password>@<host>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Connect to PostgreSQL database for psycopg2 (to run RAW SQL QUERY)
# while True:
#     # Connect to your postgres DB
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'apidev', user = 'postgres', password = 'rootuser', cursor_factory = RealDictCursor)
#         # Open a cursor to perform database operations
#         cursor = conn.cursor()
#         print("Database connection established")
#         break
#     except Exception as e:
#         print(f"Error connecting to the database: {e}")
#         time.sleep(2)