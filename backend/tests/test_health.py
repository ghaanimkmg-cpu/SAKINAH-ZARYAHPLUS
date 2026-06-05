from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json() == {
        'status': 'ok',
        'service': 'NIS Backend',
        'version': 'v1'
    }

def test_root_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {
        'status': 'ok',
        'service': 'NIS Backend',
        'version': 'v1'
    }
