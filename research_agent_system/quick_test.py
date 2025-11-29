import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f" {endpoint}: Status {response.status_code}")
        return response.json()
    except Exception as e:
        print(f" {endpoint}: {e}")
        return None

# Test endpoints
print("🧪 Quick API Test")
print("=" * 40)

health = test_endpoint("/health")
if health:
    print(f"   Status: {health['status']}")

status = test_endpoint("/status")
if status:
    print(f"   Active Tasks: {status['active_tasks']}")

tasks = test_endpoint("/tasks")
if tasks:
    print(f"   Total Tasks: {tasks['total_tasks']}")

# Test creating a research task
try:
    research_data = {
        "topic": "Machine Learning Applications",
        "content_type": "article",
        "tone": "professional",
        "length": "medium"
    }
    response = requests.post(f"{BASE_URL}/research", json=research_data)
    if response.status_code == 200:
        task_info = response.json()
        print(f" Research task created: {task_info['task_id']}")
        
        # Check the task status
        task_status = test_endpoint(f"/tasks/{task_info['task_id']}")
        if task_status:
            print(f"   Task Status: {task_status['status']}")
    else:
        print(f" Failed to create research task: {response.status_code}")
except Exception as e:

    print(f" Research task creation failed: {e}")
