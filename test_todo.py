"""
Simple test script to verify the todo app functionality
"""

import os
import sys
import json
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from todo import TodoStorage, TodoManager, TodoValidator, TodoFormatter


def test_todo_storage():
    """Test TodoStorage functionality."""
    print("Testing TodoStorage...")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        storage = TodoStorage(temp_filename)
        
        todos = storage.load_todos()
        assert todos == [], "Empty file should return empty list"
        
        test_todos = [
            {"task": "Test task", "completed": False, "created": "2024-01-01 12:00"}
        ]
        storage.save_todos(test_todos)
        loaded_todos = storage.load_todos()
        assert loaded_todos == test_todos, "Loaded todos should match saved todos"
        
        print("TodoStorage tests passed!")
        
    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_todo_validator():
    """Test TodoValidator functionality."""
    print("Testing TodoValidator...")
    
    assert TodoValidator.validate_task_text("Valid task") == True
    assert TodoValidator.validate_task_text("") == False
    assert TodoValidator.validate_task_text("   ") == False
    assert TodoValidator.validate_task_text(None) == False
    
    todos = [{"task": "Task 1"}, {"task": "Task 2"}]
    assert TodoValidator.validate_task_index(todos, 1) == True
    assert TodoValidator.validate_task_index(todos, 2) == True
    assert TodoValidator.validate_task_index(todos, 0) == False
    assert TodoValidator.validate_task_index(todos, 3) == False
    
    assert TodoValidator.get_valid_task_index(todos, "1") == 1
    assert TodoValidator.get_valid_task_index(todos, "invalid") is None
    assert TodoValidator.get_valid_task_index(todos, "0") is None
    
    print("TodoValidator tests passed!")


def test_todo_manager():
    """Test TodoManager functionality."""
    print("Testing TodoManager...")
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_filename = temp_file.name
    
    try:
        storage = TodoStorage(temp_filename)
        manager = TodoManager(storage)
        
        with patch('builtins.print'):
            result = manager.add_task("Test task")
            assert result == True, "Should successfully add valid task"
            
            result = manager.add_task("")
            assert result == False, "Should reject empty task"
        
        with patch('builtins.print'):
            result = manager.complete_task("1")
            assert result == True, "Should successfully complete task"
            
            result = manager.complete_task("1")
            assert result == False, "Should not complete already completed task"
            
            result = manager.complete_task("invalid")
            assert result == False, "Should reject invalid index"
        
        print("TodoManager tests passed!")
        
    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_todo_formatter():
    """Test TodoFormatter functionality."""
    print("Testing TodoFormatter...")
    
    colored_text = TodoFormatter.colorize("test", "green")
    assert colored_text.startswith('\033[92m'), "Should start with green color code"
    assert colored_text.endswith('\033[0m'), "Should end with reset code"
    
    todo = {
        "task": "Test task",
        "completed": False,
        "created": "2024-01-01 12:00"
    }
    formatted = TodoFormatter.format_todo_item(todo, 1)
    assert "Test task" in formatted, "Should contain task text"
    assert "2024-01-01 12:00" in formatted, "Should contain creation date"
    
    print("TodoFormatter tests passed!")


def run_integration_test():
    """Run a simple integration test."""
    print("Running integration test...")
    
    test_file = "test_todos.json"
    if os.path.exists(test_file):
        os.unlink(test_file)
    
    try:
        with patch('sys.argv', ['todo.py', 'add', 'Integration test task']):
            with patch('builtins.print'):
                from todo import main
                storage = TodoStorage(test_file)
                manager = TodoManager(storage)
                manager.add_task("Integration test task")
        
        storage = TodoStorage(test_file)
        todos = storage.load_todos()
        assert len(todos) == 1, "Should have one task"
        assert todos[0]['task'] == "Integration test task", "Task should match"
        
        print("Integration test passed!")
        
    finally:
        if os.path.exists(test_file):
            os.unlink(test_file)


def main():
    """Run all tests."""
    print("Running Todo App Tests...\n")
    
    try:
        test_todo_storage()
        test_todo_validator()
        test_todo_manager()
        test_todo_formatter()
        run_integration_test()
        
        print("\nAll tests passed! The todo app is working correctly.")
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
