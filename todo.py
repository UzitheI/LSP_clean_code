"""
CLI Todo App - A beautiful command-line todo application built for my clean code assignment
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional


class TodoStorage:
    """Handles persistent storage of todos in JSON format."""
    
    def __init__(self, filename: str = "todos.json"):
        self.filename = filename
    
    def load_todos(self) -> List[Dict]:
        """Load todos from JSON file."""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_todos(self, todos: List[Dict]) -> None:
        """Save todos to JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(todos, file, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error saving todos: {e}")
            sys.exit(1)


class TodoFormatter:
    """Handles formatting and display of todo items."""
    
    COLORS = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'reset': '\033[0m'
    }
    
    SYMBOLS = {
        'check': '✅',
        'cross': '❌',
        'list': '📋',
        'trash': '🗑️',
        'empty': '📭',
        'add': '➕',
        'todo': '📝',
        'done': '☑️',
        'pending': '⏳'
    }
    
    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Apply color to text."""
        return f"{cls.COLORS.get(color, '')}{text}{cls.COLORS['reset']}"
    
    @classmethod
    def format_todo_item(cls, todo: Dict, index: int) -> str:
        """Format a single todo item for display."""
        status = "✓" if todo['completed'] else " "
        status_color = "green" if todo['completed'] else "yellow"
        
        checkbox = cls.colorize(f"[{status}]", status_color)
        
        task_text = todo['task']
        if todo['completed']:
            task_text = cls.colorize(task_text, "green")
        
        date_str = cls.colorize(f"({todo['created']})", "blue")
        
        return f"{cls.colorize(str(index), 'magenta')}. {checkbox} {task_text} {date_str}"
    
    @classmethod
    def print_header(cls, title: str) -> None:
        """Print a beautiful header."""
        print(f"\n{cls.SYMBOLS['todo']} {cls.colorize(title, 'bold')}")
        print(cls.colorize("=" * (len(title) + 3), 'cyan'))
    
    @classmethod
    def print_success(cls, message: str) -> None:
        """Print a success message."""
        print(f"{cls.SYMBOLS['check']} {cls.colorize(message, 'green')}")
    
    @classmethod
    def print_error(cls, message: str) -> None:
        """Print an error message."""
        print(f"{cls.SYMBOLS['cross']} {cls.colorize(message, 'red')}")
    
    @classmethod
    def print_info(cls, message: str) -> None:
        """Print an info message."""
        print(f"{cls.SYMBOLS['list']} {cls.colorize(message, 'blue')}")


class TodoValidator:
    """Validates todo operations and user input."""
    
    @staticmethod
    def validate_task_text(task: str) -> bool:
        """Validate that task text is not empty."""
        return bool(task and task.strip())
    
    @staticmethod
    def validate_task_index(todos: List[Dict], index: int) -> bool:
        """Validate that task index is within valid range."""
        return 1 <= index <= len(todos)
    
    @staticmethod
    def get_valid_task_index(todos: List[Dict], index_str: str) -> Optional[int]:
        """Get a valid task index from string input."""
        try:
            index = int(index_str)
            if TodoValidator.validate_task_index(todos, index):
                return index
            return None
        except ValueError:
            return None


class TodoManager:
    """Core todo management functionality."""
    
    def __init__(self, storage: TodoStorage):
        self.storage = storage
    
    def create_todo(self, task: str) -> Dict:
        """Create a new todo item."""
        return {
            'task': task.strip(),
            'completed': False,
            'created': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
    
    def add_task(self, task: str) -> bool:
        """Add a new task to the todo list."""
        if not TodoValidator.validate_task_text(task):
            TodoFormatter.print_error("Task cannot be empty!")
            return False
        
        todos = self.storage.load_todos()
        new_todo = self.create_todo(task)
        todos.append(new_todo)
        self.storage.save_todos(todos)
        
        TodoFormatter.print_success(f"Task added: {task}")
        return True
    
    def list_tasks(self) -> None:
        """List all tasks with beautiful formatting."""
        todos = self.storage.load_todos()
        
        if not todos:
            TodoFormatter.print_info("No tasks found.")
            print(f"{TodoFormatter.SYMBOLS['empty']} Your todo list is empty!")
            return
        
        TodoFormatter.print_header("Your Todo List")
        
        pending_tasks = [todo for todo in todos if not todo['completed']]
        completed_tasks = [todo for todo in todos if todo['completed']]
        
        if pending_tasks:
            print(f"\n{TodoFormatter.SYMBOLS['pending']} {TodoFormatter.colorize('Pending Tasks:', 'yellow')}")
            for i, todo in enumerate(pending_tasks, 1):
                print(f"  {TodoFormatter.format_todo_item(todo, i)}")
        
        if completed_tasks:
            print(f"\n{TodoFormatter.SYMBOLS['done']} {TodoFormatter.colorize('Completed Tasks:', 'green')}")
            start_index = len(pending_tasks) + 1
            for i, todo in enumerate(completed_tasks, start_index):
                print(f"  {TodoFormatter.format_todo_item(todo, i)}")
        
        total = len(todos)
        completed = len(completed_tasks)
        pending = len(pending_tasks)
        print(f"\n{TodoFormatter.colorize('Summary:', 'bold')} {total} total, {completed} completed, {pending} pending")
    
    def complete_task(self, index_str: str) -> bool:
        """Mark a task as complete."""
        todos = self.storage.load_todos()
        
        if not todos:
            TodoFormatter.print_error("No tasks found!")
            return False
        
        index = TodoValidator.get_valid_task_index(todos, index_str)
        if index is None:
            TodoFormatter.print_error(f"Invalid task number: {index_str}")
            return False
        
        todo = todos[index - 1]
        if todo['completed']:
            TodoFormatter.print_info(f"Task {index} is already completed!")
            return False
        
        todos[index - 1]['completed'] = True
        self.storage.save_todos(todos)
        
        TodoFormatter.print_success(f"Task {index} marked as complete: {todo['task']}")
        return True
    
    def remove_task(self, index_str: str) -> bool:
        """Remove a task from the list."""
        todos = self.storage.load_todos()
        
        if not todos:
            TodoFormatter.print_error("No tasks found!")
            return False
        
        index = TodoValidator.get_valid_task_index(todos, index_str)
        if index is None:
            TodoFormatter.print_error(f"Invalid task number: {index_str}")
            return False
        
        removed_todo = todos.pop(index - 1)
        self.storage.save_todos(todos)
        
        TodoFormatter.print_success(f"Task {index} removed: {removed_todo['task']}")
        return True
    
    def clear_completed(self) -> bool:
        """Remove all completed tasks."""
        todos = self.storage.load_todos()
        completed_count = sum(1 for todo in todos if todo['completed'])
        
        if completed_count == 0:
            TodoFormatter.print_info("No completed tasks to clear!")
            return False
        
        todos = [todo for todo in todos if not todo['completed']]
        self.storage.save_todos(todos)
        
        TodoFormatter.print_success(f"Cleared {completed_count} completed task(s)")
        return True


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="A beautiful CLI Todo App following Clean Code Principles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Buy groceries"          Add a new task
  %(prog)s list                         List all tasks
  %(prog)s complete 1                   Mark task 1 as complete
  %(prog)s remove 1                     Remove task 1
  %(prog)s clear                        Clear all completed tasks
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('task', help='Task description')
    
    subparsers.add_parser('list', help='List all tasks')
    
    complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
    complete_parser.add_argument('index', help='Task number to complete')
    
    remove_parser = subparsers.add_parser('remove', help='Remove a task')
    remove_parser.add_argument('index', help='Task number to remove')
    
    subparsers.add_parser('clear', help='Clear all completed tasks')
    
    return parser


def main() -> None:
    """Main application entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    storage = TodoStorage()
    todo_manager = TodoManager(storage)
    
    if args.command == 'add':
        todo_manager.add_task(args.task)
    elif args.command == 'list':
        todo_manager.list_tasks()
    elif args.command == 'complete':
        todo_manager.complete_task(args.index)
    elif args.command == 'remove':
        todo_manager.remove_task(args.index)
    elif args.command == 'clear':
        todo_manager.clear_completed()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
