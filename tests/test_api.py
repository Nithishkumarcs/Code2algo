"""
Integration API tests for Flask server app.py
"""

import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['app'] == 'Code2Algo'

def test_examples_endpoint(client):
    rv = client.get('/api/examples')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['success'] is True
    assert 'python_factorial' in json_data['examples']

def test_generate_endpoint_success(client):
    payload = {
        "language": "python",
        "code": "def hello():\n    print('Hello World')",
        "detail_level": "professional"
    }
    rv = client.post('/api/generate', data=json.dumps(payload), content_type='application/json')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['success'] is True
    assert 'algorithm' in data
    assert 'pseudocode' in data
    assert 'time_complexity' in data
    assert data['detail_level'] == 'professional'

def test_generate_endpoint_empty_code(client):
    payload = {
        "language": "python",
        "code": "   ",
        "detail_level": "medium"
    }
    rv = client.post('/api/generate', data=json.dumps(payload), content_type='application/json')
    assert rv.status_code == 400
    data = rv.get_json()
    assert data['success'] is False
    assert "empty" in data['error'].lower()

def test_generate_endpoint_auto_detection(client):
    payload = {
        "language": "auto",
        "code": "#include <stdio.h>\n#include <stdint.h>\nuint16_t swap(uint16_t val) { return (val << 8) | (val >> 8); }",
        "detail_level": "professional"
    }
    rv = client.post('/api/generate', data=json.dumps(payload), content_type='application/json')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['success'] is True
    assert data['detected_info']['language'] == 'C'
    assert 'swap' in data['detected_info']['functions']

