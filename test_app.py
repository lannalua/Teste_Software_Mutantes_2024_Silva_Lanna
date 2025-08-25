import pytest
import requests
import json
from app import app, tasks
import subprocess
import sys
import time
import threading

# To run: coverage run -m pytest -s test_app.py -v
# TO see covarege: covarege html

BASE_URL = 'http://127.0.0.1:5000'

@pytest.fixture(scope="session", autouse=True)
def start_server():
    def run_server():
        app.run(debug=False, port=5000, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(2) 
    yield

@pytest.fixture(autouse=True)
def cleanup_tasks():
    original_tasks = tasks.copy()
    
    yield
    
    tasks.clear()
    tasks.extend(original_tasks)

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
    assert response_json["message"] == "Nova tarefa criada com sucesso"

def test_create_task_without_description():
    new_task_data = {
        "title": "Tarefa sem descrição"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json

# def test_create_task_missing_title():
#     new_task_data = {
#         "description": "Sem título"
#     }
#     response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
#     assert response.status_code == 500

# def test_create_task_empty_json():
#     response = requests.post(f"{BASE_URL}/tasks", json={})
#     assert response.status_code == 500

# def test_get_tasks_empty():
#     tasks.clear()
    
#     response = requests.get(f"{BASE_URL}/tasks")
#     assert response.status_code == 200
#     response_json = response.json()
#     assert "tasks" in response_json
#     assert "total_tasks" in response_json
#     assert response_json["total_tasks"] == 0
#     assert len(response_json["tasks"]) == 0

def test_get_tasks_with_data():
    task_data_1 = {"title": "Tarefa 1", "description": "Desc 1"}
    task_data_2 = {"title": "Tarefa 2", "description": "Desc 2"}
    
    requests.post(f"{BASE_URL}/tasks", json=task_data_1)
    requests.post(f"{BASE_URL}/tasks", json=task_data_2)
    
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["total_tasks"] >= 2
    assert len(response_json["tasks"]) >= 2

def test_get_task_existing():
    task_data = {"title": "Tarefa para buscar", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == task_id
    assert response_json["title"] == "Tarefa para buscar"

# def test_get_task_not_found():
#     response = requests.get(f"{BASE_URL}/tasks/9999")
#     assert response.status_code == 404
#     response_json = response.json()
#     assert "message" in response_json
#     assert response_json["message"] == "Não foi possível encontrar a atividade"

def test_get_task_invalid_id():
    response = requests.get(f"{BASE_URL}/tasks/abc")
    assert response.status_code == 404

def test_update_task_complete():
    task_data = {"title": "Tarefa original", "description": "Desc original"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    payload = {
        "title": "Título atualizado",
        "description": "Descrição atualizada",
        "completed": True
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    
    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    updated_task = get_response.json()
    assert updated_task["title"] == "Título atualizado"
    assert updated_task["description"] == "Descrição atualizada"
    assert updated_task["completed"] == True

def test_update_task_partial():
    task_data = {"title": "Tarefa original", "description": "Desc original"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    original_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    original_task = original_response.json()
    assert original_task["completed"] == False
    
    payload = {
        "title": "Apenas título atualizado",
        "description": "Desc original",  # Manter original
        "completed": False  # Manter original
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    
    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    updated_task = get_response.json()
    assert updated_task["title"] == "Apenas título atualizado"
    assert updated_task["description"] == "Desc original"
    assert updated_task["completed"] == False

def test_update_task_missing_title():
    task_data = {"title": "Tarefa original", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    payload = {
        "description": "Nova descrição",
        "completed": True
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 500

def test_update_task_missing_description():
    task_data = {"title": "Tarefa original", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    payload = {
        "title": "Novo título",
        "completed": True
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 500

def test_update_task_missing_completed():
    task_data = {"title": "Tarefa original", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    payload = {
        "title": "Novo título",
        "description": "Nova descrição"
    }
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 500

# def test_update_task_not_found():
#     payload = {
#         "title": "Qualquer",
#         "description": "Qualquer",
#         "completed": False
#     }
#     response = requests.put(f"{BASE_URL}/tasks/9999", json=payload)
#     assert response.status_code == 404
#     response_json = response.json()
#     assert "message" in response_json

def test_delete_task_existing():
    task_data = {"title": "Tarefa para deletar", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response.status_code == 200
    
    delete_response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert delete_response.status_code == 200
    
    get_response_after = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert get_response_after.status_code == 404

# def test_delete_task_not_found():
#     response = requests.delete(f"{BASE_URL}/tasks/9999")
#     assert response.status_code == 404
#     response_json = response.json()
#     assert "message" in response_json

def test_delete_task_twice():
    task_data = {"title": "Tarefa dupla", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response1 = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response1.status_code == 200
    
    response2 = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response2.status_code == 404

def test_task_completed_default_false():
    task_data = {"title": "Tarefa padrão", "description": "Teste"}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = response.json()["id"]
    
    get_response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    task = get_response.json()
    assert task["completed"] == False

# def test_main_block_executes():
#     result = subprocess.run([sys.executable, "app.py", "--help"], 
#                           capture_output=True, text=True, timeout=5)
#     assert True 

# def test_invalid_json_payload():
#     response = requests.post(f"{BASE_URL}/tasks", data="invalid json")
#     assert response.status_code == 415

def test_update_task_invalid_json():
    task_data = {"title": "Tarefa teste", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", data="invalid json")
    assert response.status_code == 415

def test_task_to_dict_method():
    from app import Task
    task = Task(1, "Teste", "Descrição", True)
    task_dict = task.to_dict()
    
    expected = {
        "id": 1,
        "title": "Teste",
        "description": "Descrição",
        "completed": True
    }
    
    assert task_dict == expected

def test_task_initialization():
    from app import Task
    task = Task(1, "Título", "Descrição", True)
    assert task.id == 1
    assert task.title == "Título"
    assert task.description == "Descrição"
    assert task.completed == True
    
    task2 = Task(2, "Título2", "Descrição2")
    assert task2.completed == False

def test_update_task_find_logic():
    task_data = {"title": "Teste find", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    payload = {
        "title": "Atualizado",
        "description": "Atualizado",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
    assert response.status_code == 200

def test_delete_task_find_logic():
    task_data = {"title": "Teste delete find", "description": "Teste"}
    create_response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200

def test_task_id_auto_increment():
    original_tasks = tasks.copy()
    tasks.clear()
    
    try:
        task1_data = {"title": "Tarefa 1"}
        task2_data = {"title": "Tarefa 2"}
        task3_data = {"title": "Tarefa 3"}
        
        response1 = requests.post(f"{BASE_URL}/tasks", json=task1_data)
        response2 = requests.post(f"{BASE_URL}/tasks", json=task2_data)
        response3 = requests.post(f"{BASE_URL}/tasks", json=task3_data)
        
        ids = [response1.json()["id"], response2.json()["id"], response3.json()["id"]]
        assert ids == sorted(ids) 
        
    finally:
        tasks.clear()
        tasks.extend(original_tasks)

if __name__ == "__main__":
    pytest.main(["-v", __file__])