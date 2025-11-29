#!/usr/bin/env python3
"""
Research Agent System - API Test Script
Test all endpoints of the Research Agent System
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health Check: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Components: {', '.join(data['components'].keys())}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return False

def test_status():
    """Test status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/status")
        if response.status_code == 200:
            data = response.json()
            print_success("System Status:")
            print(f"   Status: {data['status']}")
            print(f"   Active Tasks: {data['active_tasks']}")
            print(f"   Agents Online: {', '.join(data['agents_online'])}")
            print(f"   Memory Entries: {data['memory_entries']}")
            print(f"   Active Sessions: {data['active_sessions']}")
            return True
        else:
            print_error(f"Status check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Status check failed: {e}")
        return False

def test_create_research_task():
    """Test creating a research task"""
    try:
        research_data = {
            "topic": "Artificial Intelligence in Healthcare",
            "content_type": "research_report",
            "tone": "professional",
            "length": "comprehensive",
            "depth": "detailed"
        }
        
        response = requests.post(f"{BASE_URL}/research", json=research_data)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Research Task Created: {data['task_id']}")
            print(f"   Status: {data['status']}")
            print(f"   Message: {data['message']}")
            return data['task_id']
        else:
            print_error(f"Research task creation failed with status {response.status_code}")
            return None
    except Exception as e:
        print_error(f"Research task creation failed: {e}")
        return None

def test_get_task_status(task_id):
    """Test getting task status"""
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Task Status for {task_id}:")
            print(f"   Status: {data['status']}")
            print(f"   Topic: {data['request']['topic']}")
            
            if data['status'] == 'completed' and 'result' in data:
                result = data['result']
                if 'research' in result:
                    print(f"   Research Content: {len(result['research']['content'])} characters")
                if 'content' in result:
                    print(f"   Generated Content: {len(result['content'])} characters")
                if 'analysis' in result:
                    print(f"   Analysis Completed: Yes")
            
            return True
        else:
            print_error(f"Task status check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Task status check failed: {e}")
        return False

def test_list_tasks():
    """Test listing all tasks"""
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Task List: {data['total_tasks']} total tasks")
            
            for task in data['tasks'][:3]:  # Show first 3 tasks
                print(f"   - {task['task_id']}: {task['topic']} ({task['status']})")
            
            return True
        else:
            print_error(f"Task list failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Task list failed: {e}")
        return False

def test_metrics():
    """Test metrics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        if response.status_code == 200:
            print_success("Metrics endpoint working")
            # Metrics are in Prometheus format, just check if we get content
            if len(response.text) > 0:
                print("   Metrics data received successfully")
            return True
        else:
            print_error(f"Metrics endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Metrics endpoint failed: {e}")
        return False

def test_memory_stats():
    """Test memory statistics"""
    try:
        response = requests.get(f"{BASE_URL}/memory/stats")
        if response.status_code == 200:
            data = response.json()
            print_success("Memory Statistics:")
            print(f"   Total Memories: {data.get('total_memories', 0)}")
            print(f"   Storage Backend: {data.get('storage_backend', 'unknown')}")
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print_error(f"Memory stats failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Memory stats failed: {e}")
        return False

def test_session_stats():
    """Test session statistics"""
    try:
        response = requests.get(f"{BASE_URL}/sessions/stats")
        if response.status_code == 200:
            data = response.json()
            print_success("Session Statistics:")
            print(f"   Total Sessions: {data.get('total_sessions', 0)}")
            return True
        else:
            print_error(f"Session stats failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Session stats failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Research Agent System - API Test Suite")
    print("=" * 50)
    
    # Check if server is running
    print_info("Testing API endpoints...")
    print()
    
    # Run all tests
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Health check
    if test_health():
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 2: Status check
    if test_status():
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 3: Create research task
    task_id = test_create_research_task()
    if task_id:
        tests_passed += 1
        
        # Wait a bit for task processing
        print_info("Waiting for task processing...")
        time.sleep(2)
        
        # Test 4: Get task status
        if test_get_task_status(task_id):
            tests_passed += 1
        else:
            tests_failed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 5: List tasks
    if test_list_tasks():
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 6: Metrics
    if test_metrics():
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 7: Memory stats
    if test_memory_stats():
        tests_passed += 1
    else:
        tests_failed += 1
    print()
    
    # Test 8: Session stats
    if test_session_stats():
        tests_passed += 1
    else:
        tests_failed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    
    if tests_failed == 0:
        print_success("All tests passed! 🎉")
        print("\n🚀 System is ready for use!")
        print("   Visit http://localhost:8000/docs for interactive API documentation")
    else:
        print_error("Some tests failed. Please check the server logs.")
        sys.exit(1)

if __name__ == "__main__":
    main()