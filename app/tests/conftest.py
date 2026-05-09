import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.infrastructure.database import Base, get_db
import uuid
import os
from dotenv import load_dotenv

# ==========================================================================================
load_dotenv()

TEST_DATABASE_URL = os.getenv('DATABASE_URL_TEST')
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind= engine
)
# ==========================================================================================
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
# ==========================================================================================


@pytest.fixture(scope="session" , autouse=True)
def setup_database():
    Base.metadata.create_all(bind = engine)

    yield
    
    Base.metadata.drop_all(bind = engine)
    
@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides = {}
    
# ==========================================================================================

@pytest.fixture
def create_user(client):
    def _create(username = 'user1test', password = "user1password", role = 'user' ):
        
        response = client.post(
            '/register', json={
                "username": username ,
                "password" : password,
                "role" : role})
        assert response.status_code in [200, 201]
        return {
                "username": response.json()['username'] ,
                'id' : response.json()['id'],
                "role" : response.json()['role']}
    return _create



@pytest.fixture
def get_token(client, create_user):
    def _get_token(username='user1test', password = 'user1password', role = 'user'):

        create_user(username, password, role)

        res = client.post('/login', data ={
            'username' :username,
            'password': password
        })
        return res.json()['access_token']
                
    return _get_token



@pytest.fixture
def only_get_token(client):
    def _get_token(username, password ):

        res = client.post('/login', data ={
            'username' :username,
            'password': password
        })
        assert res.status_code ==200
        return res.json()['access_token']
                
    return _get_token

@pytest.fixture
def auth_header(get_token):
    def _auth(username, password, role):
        token = get_token(username, password, role)
        return {"Authorization" : f"Bearer {token}"}
    return _auth

@pytest.fixture
def create_a_todo(client):
    def _create_todo(title = 'title1test', description = 'description1test', priority = 'low' , headers = None):
        
        response = client.post('/todos/create_todo', json={
            'title' : title,
            'description' : description,
            'priority' : priority},
             headers= headers              
        )
        assert response.status_code == 200
        return response.json()
    return _create_todo



# ==========================================================================================







