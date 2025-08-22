import pytest
import requests
import app
import subprocess
import sys


BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']

def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "Nova descrição",
            "title": "Título atualizado"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]

def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404

def test_create_task_missing_title():
    new_task_data = {
        "description": "Sem título"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 500

def test_update_task_invalid_payload():

    new_task = {"title": "Teste inválido", "description": "Teste"}
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    assert response.status_code == 200
    task_id = response.json()["id"]

    payload = {"title": "Sem descrição"} 
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)

    assert response.status_code == 500


def test_main_block_executes():
    result = subprocess.run([sys.executable, "app.py"], capture_output=True, timeout=2)
    assert result.returncode in (0, 1, -15, None)

def test_get_task_not_found():
    response = requests.get(f"{BASE_URL}/tasks/9999")
    assert response.status_code == 404
    response_json = response.json()
    assert "message" in response_json
    assert response_json["message"] == "Não foi possível encontrar a atividade"

def test_update_task_not_found():
    payload = {
        "title": "Qualquer",
        "description": "Qualquer",
        "completed": False
    }
    response = requests.put(f"{BASE_URL}/tasks/9999", json=payload)
    assert response.status_code == 404
    response_json = response.json()
    assert "message" in response_json

def test_update_task_missing_completed():
    new_task = {"title": "Task sem completed", "description": "desc"}
    response = requests.post(f"{BASE_URL}/tasks", json=new_task)
    assert response.status_code == 200
    task_id = response.json()["id"]

    payload = {"title": "Atualizada", "description": "desc nova"} 
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 500

def test_delete_task_not_found():
    response = requests.delete(f"{BASE_URL}/tasks/9999")
    assert response.status_code == 404
    response_json = response.json()
    assert "message" in response_json

