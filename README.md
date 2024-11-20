# Script Manager

[中文](README-CN.md) | English

A Windows desktop application for managing and executing various types of scripts.

## Key Features

### Script Management
- Add, edit, delete and organize multiple types of script files (Python, Node.js, Shell, etc.)
- Categorize scripts by purpose and type
- Script version control with history tracking
- Import/Export script configurations

### Visual Execution
- User-friendly GUI, no command line needed
- Smart parameter recognition with auto-generated input forms
- Support parameter default values and descriptions
- Save and reuse common parameter combinations

### Execution Management
- Real-time script execution status and output logs
- Support interrupting running scripts
- Execution history with parameter info and results
- Script execution timeout settings
- Exception handling and error logging

### Additional Features
- Multi-user support with script isolation
- Permission control for script access and execution
- Environment variable and dependency management
- API interface for external system calls
- Theme switching (Dark/Light mode)
- Multi-language support (English/Chinese)

## Use Cases
- DevOps automation tool management
- Data processing script management
- Batch test case execution
- Scheduled task management
- Development utility integration

## Technical Features
- Developed with Python 3 and PyQt6 for modern UI
- SQLite local storage for lightweight efficiency
- Modular design for easy extension
- Built-in script execution engine
- Unified logging and exception handling

## Installation

1. Clone the repository:
   `git clone https://github.com/yourusername/script-manager.git`

2. Install dependencies:
   `pip install -r requirements.txt`

3. Run the application:
   `python main.py`

## Development

1. Create virtual environment:
   `python -m venv venv`

2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install development dependencies:
   `pip install -r requirements-dev.txt`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
