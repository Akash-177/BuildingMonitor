import pytest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_get_buildings(client):
    resp = client.get('/api/buildings')
    assert resp.status_code == 200

def test_create_building(client):
    resp = client.post('/api/buildings', 
        json={'name': 'Test Building', 'location': 'Test City'}
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == 'Test Building'

def test_get_equipment(client):
    resp = client.get('/api/equipment')
    assert resp.status_code == 200

def test_create_equipment(client):
    # create building first
    bldg_resp = client.post('/api/buildings',
        json={'name': 'Test Bldg', 'location': 'Cork'}
    )
    bldg_id = bldg_resp.get_json()['id']
    
    # then equipment
    resp = client.post('/api/equipment',
        json={
            'building_id': bldg_id,
            'name': 'Test HVAC',
            'type': 'HVAC',
            'model': 'Test'
        }
    )
    assert resp.status_code == 201

def test_sensor_post(client):
    resp = client.post('/api/sensors',
        json={
            'equipment_id': 1,
            'temperature': 72.5,
            'vibration': 1.5,
            'runtime_hours': 4500
        }
    )
    assert resp.status_code == 201

def test_equipment_health(client):
    resp = client.get('/api/equipment/1/health')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'status' in data