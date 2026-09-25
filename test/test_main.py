from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy.orm import sessionmaker
import pytest
from sqlalchemy import create_engine


#SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:180598@localhost:5432/fastapi_test'
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

Test_SessionLocal =sessionmaker(autocommit=False, autoflush= False, bind= engine)

def Test_get_db():
    db = Test_SessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = Test_get_db


@pytest.fixture

def test():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_root(test):
    res = test.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to Library'

def test_create_user(test):
    res = test.post("/users/",json={"name": "lakith", "username" : "lakith", "email" : "lakith@gmail.com" ,"password" : "Lakveth@180598"})
    new_user = schemas.responseuser(**res.json())
    assert new_user.username == "lakith"
    assert res.status_code == 201