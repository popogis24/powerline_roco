import os
import pytest
from src.notificator import EmailNotification


@pytest.fixture(scope="module")
def test_email(self):













@pytest.fixture(scope="module")
def setup_database():
    
    db_url = 'sqlite:///test_broker.db'
    
    # Delete the database file if it already exists
    if os.path.exists('test_broker.db'):
        os.remove('test_broker.db')
    
    local_db = LocalDatabase(db_url)
    local_db.setup()
    yield db_url
    local_db.cleanup()
    local_db.db_manager.engine.dispose()  # Close the database connection

@pytest.fixture(scope="module")
def coordinator_service(setup_database):
    coordinator_api = CoordinatorAPI(setup_database)
    config = uvicorn.Config(coordinator_api, host="localhost", port=5001)
    server = uvicorn.Server(config)
    coordinator_thread = threading.Thread(target=server.run)
    coordinator_thread.start()
    time.sleep(2)
    yield server
    server.should_exit = True
    coordinator_thread.join()

@pytest.fixture(scope="module")
def worker_service(setup_database, coordinator_service):
    worker_api = WorkerAPI('http://localhost:5001', "test_worker", "127.0.0.1", 4, 8)
    config = uvicorn.Config(worker_api, host="localhost", port=8001)
    server = uvicorn.Server(config)
    worker_thread = threading.Thread(target=server.run)
    worker_thread.start()
    time.sleep(2)
    yield server
    server.should_exit = True
    worker_thread.join()

def test_monitor_workers(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    response = requests.get(f'{coordinator_url}/monitor_workers')
    assert response.status_code == 200

def test_delete_all_tasks(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    response = requests.get(f'{coordinator_url}/get_all_tasks')
    assert response.status_code == 200
    tasks_data = response.json()
    for task_data in tasks_data:
        task_id = task_data["globalid"]
        response = requests.delete(f'{coordinator_url}/delete_task/{task_id}')
        assert response.status_code == 200

    response = requests.get(f'{coordinator_url}/get_all_tasks')
    assert response.status_code == 200
    assert len(response.json()) == 0

def test_create_tasks(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    tasks_data = [
        {"globalid": "{621DE74B-D241-4658-AA0A-E4A0648E4C75}", "algorithm": "fire", "idbditlt": "{569443DD-9D1D-4335-A04D-B9C5522C627C}"},
        {"globalid": "{ABE33B33-E6BC-40DF-82A6-FF665C55C686}", "algorithm": "fire", "idbditlt": "{A5433A82-5414-4036-BDBE-D3529846DB3A}"},
        {"globalid": "{83738D3D-8178-408A-B12E-8F5AF7F18849}", "algorithm": "fire", "idbditlt": "{0B55F8E0-EDF2-4759-8EF9-68F2164C7A8F}"}
    ]
    for task_data in tasks_data:
        response = requests.post(f'{coordinator_url}/create_task', json=task_data)
        assert response.status_code == 200

def test_get_task(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    task_id = "{621DE74B-D241-4658-AA0A-E4A0648E4C75}"
    response = requests.get(f'{coordinator_url}/get_task/{task_id}')
    assert response.status_code == 200
    assert response.json()["globalid"] == task_id

def test_assign_tasks(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    tasks_data = [
        {"globalid": "{621DE74B-D241-4658-AA0A-E4A0648E4C75}", "algorithm": "fire", "idbditlt": "{569443DD-9D1D-4335-A04D-B9C5522C627C}"},
        {"globalid": "{ABE33B33-E6BC-40DF-82A6-FF665C55C686}", "algorithm": "fire", "idbditlt": "{A5433A82-5414-4036-BDBE-D3529846DB3A}"},
        {"globalid": "{83738D3D-8178-408A-B12E-8F5AF7F18849}", "algorithm": "fire", "idbditlt": "{0B55F8E0-EDF2-4759-8EF9-68F2164C7A8F}"}
    ]
    for _ in range(len(tasks_data)):
        response = requests.get(f'{coordinator_url}/assign_task')
        assert response.status_code == 200

def test_tasks_done(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    tasks_data = [
        {"globalid": "{621DE74B-D241-4658-AA0A-E4A0648E4C75}", "algorithm": "fire", "idbditlt": "{569443DD-9D1D-4335-A04D-B9C5522C627C}"},
        {"globalid": "{ABE33B33-E6BC-40DF-82A6-FF665C55C686}", "algorithm": "fire", "idbditlt": "{A5433A82-5414-4036-BDBE-D3529846DB3A}"},
        {"globalid": "{83738D3D-8178-408A-B12E-8F5AF7F18849}", "algorithm": "fire", "idbditlt": "{0B55F8E0-EDF2-4759-8EF9-68F2164C7A8F}"}
    ]
    for task_data in tasks_data:
        task_id = task_data["globalid"]
        response = requests.get(f'{coordinator_url}/get_task/{task_id}')
        assert response.status_code == 200
        assert response.json()["status"] == "DONE"

def test_update_task(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    task_id = "{621DE74B-D241-4658-AA0A-E4A0648E4C75}"
    update_data = {"status": "UPDATED"}
    response = requests.put(f'{coordinator_url}/update_task/{task_id}', json=update_data)
    assert response.status_code == 200

    response = requests.get(f'{coordinator_url}/get_task/{task_id}')
    assert response.status_code == 200
    assert response.json()["status"] == "UPDATED"

def test_delete_task(setup_database, coordinator_service, worker_service):
    coordinator_url = 'http://localhost:5001'
    task_id = "{621DE74B-D241-4658-AA0A-E4A0648E4C75}"
    response = requests.delete(f'{coordinator_url}/delete_task/{task_id}')
    assert response.status_code == 200

    response = requests.get(f'{coordinator_url}/get_task/{task_id}')
    assert response.status_code == 404