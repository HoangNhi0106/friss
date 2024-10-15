import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.core.config import settings
from psycopg2 import connect, sql

def init_db():
    conn = connect(
        dbname='postgres',
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    test_db_name = 'test_friss'

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (test_db_name,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(test_db_name)))

    cursor.close()
    conn.close()

def create_extensions(test_db_url):
    conn = connect(test_db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    cursor.close()
    conn.close()

@pytest.fixture(scope="session")
def test_db():
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/test_friss"

    create_extensions(DATABASE_URL)
    
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)

    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

