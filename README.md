# 📝 Beautiful CLI Todo App

A stunning command-line Todo application written in **Python**, meticulously crafted following **Clean Code Principles**. Features beautiful terminal output with colors, Unicode symbols, and an intuitive interface. This is done as a part of Leapfrog Partnership Program.

---

## ✨ Features

- ✅ **Add tasks** - Create new todo items with timestamps
- 📋 **List tasks** - View all tasks with beautiful formatting, separated by status
- ☑️ **Complete tasks** - Mark tasks as complete with visual feedback
- 🗑️ **Remove tasks** - Delete individual tasks
- 🧹 **Clear completed** - Remove all completed tasks at once
- 💾 **Persistent storage** - Tasks saved in JSON format
- 🎨 **Beautiful output** - Colorized terminal output with Unicode symbols
- 📊 **Task summary** - Shows total, completed, and pending task counts

---

## 🎨 Beautiful Interface

The app features:
- **Colorized output** with different colors for different states
- **Unicode symbols** for visual appeal (✅ ❌ 📋 🗑️ 📭 ➕ 📝)
- **Organized display** with pending and completed tasks separated
- **Task summaries** with counts and statistics
- **Timestamps** showing when tasks were created

---

## 🧑‍💻 Usage Examples

### Adding Tasks
```bash
$ python todo.py add "Buy groceries"
✅ Task added: Buy groceries

$ python todo.py add "Read Clean Code book"
✅ Task added: Read Clean Code book
```

### Listing Tasks
```bash
$ python todo.py list

📝 Your Todo List
==================

⏳ Pending Tasks:
  1. [ ] Buy groceries (2024-01-15 10:30)
  2. [ ] Read Clean Code book (2024-01-15 10:31)

Summary: 2 total, 0 completed, 2 pending
```

### Completing Tasks
```bash
$ python todo.py complete 1
✅ Task 1 marked as complete: Buy groceries

$ python todo.py list

📝 Your Todo List
==================

⏳ Pending Tasks:
  1. [ ] Read Clean Code book (2024-01-15 10:31)

☑️ Completed Tasks:
  2. [✓] Buy groceries (2024-01-15 10:30)

Summary: 2 total, 1 completed, 1 pending
```

### Removing Tasks
```bash
$ python todo.py remove 1
✅ Task 1 removed: Read Clean Code book
```

### Clearing Completed Tasks
```bash
$ python todo.py clear
✅ Cleared 1 completed task(s)
```

### Getting Help
```bash
$ python todo.py --help
$ python todo.py add --help
```

---

## 🧼 Clean Code Principles Applied

| Principle | Implementation |
|-----------|----------------|
| **Single Responsibility** | Each class has one clear purpose (`TodoStorage`, `TodoFormatter`, `TodoValidator`, `TodoManager`) |
| **Meaningful Names** | Clear, descriptive names for functions and variables (`add_task`, `validate_task_index`, `format_todo_item`) |
| **Small Functions** | Functions are focused and do one thing well |
| **DRY (Don't Repeat Yourself)** | Common functionality extracted into reusable methods |
| **Error Handling** | Graceful error handling with clear user feedback |
| **Consistent Formatting** | Follows PEP8 style guidelines throughout |
| **Type Hints** | Full type annotation for better code clarity |
| **Documentation** | Comprehensive docstrings for all classes and methods |
| **Separation of Concerns** | UI, business logic, and data persistence are separated |

---

## 🏗️ Architecture

```
TodoApp/
├── TodoStorage      # Handles JSON file persistence
├── TodoFormatter    # Manages colors, symbols, and display formatting
├── TodoValidator    # Validates user input and data
├── TodoManager      # Core business logic for todo operations
└── CLI Parser       # Command-line interface handling
```

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/UzitheI/cli-todo-clean.git
   cd cli-todo-clean
   ```

2. **Run the application:**
   ```bash
   python todo.py add "Your first task"
   python todo.py list
   ```

3. **Make it executable (optional):**
   ```bash
   chmod +x todo.py
   ./todo.py add "Your task"
   ```

---

## 🛠️ Requirements

- **Python 3.6+** (uses f-strings and type hints)
- **No external dependencies** - uses only Python standard library
- **Terminal with Unicode support** for best visual experience

---

## 📁 File Structure

```
├── todo.py           # Main application file
├── requirements.txt  # Dependencies (none required)
├── README.md        # This documentation
└── todos.json       # Auto-generated data file
```

---

## 🧪 Testing

The app includes robust input validation and error handling:

- **Empty task validation** - Cannot add empty tasks
- **Invalid index handling** - Clear error messages for invalid task numbers
- **File I/O error handling** - Graceful handling of file system issues
- **JSON parsing errors** - Fallback to empty todo list if file is corrupted

---

## 🎯 Future Enhancements

- 📅 Due dates and reminders
- 🏷️ Task categories and tags
- 🔍 Search and filter functionality
- 📊 Productivity statistics
- 🌐 Cloud synchronization
- 📱 Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. Code follows clean code principles
2. All functions have proper docstrings
3. Type hints are used consistently
4. PEP8 formatting is maintained

---

## 📄 License

MIT License - feel free to use this code for learning and projects.

---

## ✍️ Author

**[UzitheI](https://github.com/UzitheI)**

*Built with ❤️ following Clean Code Principles*
