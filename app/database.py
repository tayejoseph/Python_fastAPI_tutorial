
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy specific code, as with any other app
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/hostname/fastapi'
# DATABASE_URL = "postgresql://user:password@postgresserver/db"
# database = databases.Database(DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()