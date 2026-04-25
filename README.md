# DocForge

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/AST-Analysis-FF6B6B?style=for-the-badge&logo=code&logoColor=white" alt="AST Analysis">
  <img src="https://img.shields.io/badge/Output-Markdown%20%7C%20Console-009688?style=for-the-badge" alt="Output Formats">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 📝 **Auto-Documentation Generator** — Transform Python source code into beautiful, comprehensive documentation using AST analysis. Extract docstrings, type hints, decorators, and more.

## About

**DocForge** automatically generates documentation from Python source code by parsing the Abstract Syntax Tree (AST). It understands Google-style, NumPy-style, and Sphinx-style docstrings, preserving all parameter types, return values, and examples.

### Who It's For

- **Developers** — Generate API docs without writing them manually
- **Technical Writers** — Extract documentation from codebase as starting point
- **Open Source Projects** — Automate documentation generation for releases
- **Teams** — Maintain consistent documentation across the codebase

## ✨ Features

### 🔍 AST-Based Analysis
- **Deep Parsing** — Walks the entire AST to extract all code elements
- **Type Hints Preservation** — Maintains all type annotations in output
- **Decorator Tracking** — Documents decorators on functions and classes
- **Inheritance Mapping** — Shows class hierarchies and method overrides

### 📝 Docstring Support
- **Google Style** — `Args:`, `Returns:`, `Raises:`, `Examples:`
- **NumPy Style** — `Parameters`, `Returns`, `Raises`
- **Sphinx Style** — `:param:`, `:returns:`, `:raises:`

### 📤 Output Formats
- **Console Output** — Formatted text with colors and structure
- **Markdown** — GitHub-flavored Markdown with code blocks
- **HTML** — Self-contained HTML documentation (future)
- **JSON** — Machine-readable format for tooling

### 🛠️ Project Analysis
- **Directory Scanning** — Analyze entire projects at once
- **Code Statistics** — LOC, complexity, documentation coverage
- **Import Graph** — Module dependency visualization
- **Coverage Report** — Documentation coverage percentage

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                            DocForge                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                         CLI Layer                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐  │   │
│  │  │ generate │  │ analyze  │  │   init   │  │   serve     │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                     Parser Layer                              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │   │
│  │  │    AST     │  │  Docstring │  │    Type    │             │   │
│  │  │   Walker   │  │   Parser   │  │   Hints    │             │   │
│  │  └────────────┘  └────────────┘  └────────────┘             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   Generator Layer                            │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │   │
│  │  │  Console   │  │  Markdown  │  │    JSON    │             │   │
│  │  │  Renderer  │  │  Renderer  │  │  Renderer  │             │   │
│  │  └────────────┘  └────────────┘  └────────────┘             │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Installation

### Prerequisites

- Python 3.9+
- pip

### Standard Installation

```bash
# Clone the repository
git clone https://github.com/moggan1337/DocForge.git
cd DocForge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m src.cli --version
```

### Using pip

```bash
pip install docforge
```

## 🚀 Quick Start

### Generate Documentation for a File

```bash
python -m src.cli generate path/to/module.py
```

### Generate Documentation for a Project

```bash
python -m src.cli generate path/to/project --recursive
```

### Generate Markdown Output

```bash
python -m src.cli generate module.py --format markdown --output docs.md
```

### Analyze Code Statistics

```bash
python -m src.cli analyze path/to/project
```

### Initialize Project Documentation

```bash
python -m src.cli init path/to/project
```

## 📚 CLI Reference

```bash
# Generate documentation
docforge generate <path> [options]
  --output, -o          Output file path
  --format, -f          Output format (console/markdown/json)
  --verbose, -v         Verbose output
  --include-private     Include private methods/classes

# Analyze project
docforge analyze <path> [options]
  --verbose, -v         Show detailed statistics
  --output, -o          Save statistics to file

# Initialize documentation
docforge init <path>
  --template, -t        Use a template (default/minimal/full)
  --force               Overwrite existing docs

# Serve documentation
docforge serve <path>
  --port, -p            Port number (default: 8000)
  --host                Host address (default: localhost)
```

## 📝 Input Code Example

```python
from typing import Optional, List, Dict
from datetime import datetime

class UserService:
    """Service for managing users in the system.
    
    This class provides methods for creating, updating, and
    retrieving user information from the database.
    
    Attributes:
        db: Database connection instance
        cache: Optional caching layer
    """
    
    def __init__(self, db: "Database", cache: Optional["Cache"] = None):
        """Initialize the UserService.
        
        Args:
            db: Database connection instance
            cache: Optional caching layer for performance
        """
        self.db = db
        self.cache = cache
    
    def create_user(
        self,
        name: str,
        email: str,
        age: Optional[int] = None
    ) -> Dict[str, any]:
        """Create a new user in the system.
        
        Args:
            name: User's full name
            email: User's email address
            age: Optional user age
            
        Returns:
            Dictionary containing the created user data
            
        Raises:
            ValueError: If email is already registered
            ConnectionError: If database is unreachable
            
        Example:
            >>> service = UserService(db)
            >>> user = service.create_user("John", "john@example.com", 30)
            >>> print(user['id'])
            42
        """
        # Implementation here...
        return {"id": 42, "name": name, "email": email}
```

## 📤 Example Output

### Console Output

```
╔══════════════════════════════════════════════════════════════╗
║                     DocForge Output                          ║
╠══════════════════════════════════════════════════════════════╣
║  Module: user_service.py                                      ║
║  Classes: 1  │  Functions: 1  │  Lines: 45                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📦 UserService                                              ║
║  │                                                           ║
║  │  📝 """Service for managing users..."""                   ║
║  │                                                           ║
║  ├─ ⚙️ __init__(db, cache=None)                              ║
║  │     Args:                                                 ║
║  │       • db: Database connection instance                  ║
║  │       • cache: Optional caching layer                    ║
║  │                                                           ║
║  └─ ⚙️ create_user(name, email, age=None) → Dict            ║
║        Args:                                                 ║
║          • name: str — User's full name                     ║
║          • email: str — User's email address                 ║
║          • age: Optional[int] — User's age                   ║
║        Returns: Dict[str, any]                               ║
║        Raises: ValueError, ConnectionError                  ║
║        Example: >>> service.create_user("John", ...         ║
╚══════════════════════════════════════════════════════════════╝
```

### Markdown Output

```markdown
# Module: user_service.py

## Classes

### `UserService`

Service for managing users in the system.

**Attributes:**
| Name | Type | Description |
|------|------|-------------|
| `db` | `Database` | Database connection instance |
| `cache` | `Optional[Cache]` | Optional caching layer |

#### Methods

##### `__init__(db, cache=None)`

Initialize the UserService.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `db` | `Database` | — | Database connection instance |
| `cache` | `Optional[Cache]` | `None` | Optional caching layer |

##### `create_user(name, email, age=None) -> Dict[str, any]`

Create a new user in the system.

**Parameters:**
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str` | — | User's full name |
| `email` | `str` | — | User's email address |
| `age` | `Optional[int]` | `None` | Optional user age |

**Returns:** Dictionary containing the created user data

**Raises:**
- `ValueError`: If email is already registered
- `ConnectionError`: If database is unreachable

**Example:**
```python
>>> service = UserService(db)
>>> user = service.create_user("John", "john@example.com", 30)
>>> print(user['id'])
42
```
```

## 📊 Project Statistics

```bash
$ docforge analyze my_project --verbose

┌─────────────────────────────────────────────────────┐
│  Project Analysis: my_project                       │
├─────────────────────────────────────────────────────┤
│  Files:                42                            │
│  Lines of Code:        3,847                         │
│  Classes:              156                          │
│  Functions:            423                          │
│  Documentation Coverage:  67.3%                     │
├─────────────────────────────────────────────────────┤
│  Modules without docs:    8                          │
│  Classes without docs:   23                         │
│  Functions without docs: 89                          │
└─────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
DocForge/
├── src/
│   ├── __init__.py
│   ├── cli.py              # Click-based CLI interface
│   └── generator.py        # AST analysis and rendering
├── tests/
│   └── test_generator.py   # Unit tests
├── docs/                   # Documentation
│   ├── installation.md
│   ├── usage.md
│   └── configuration.md
├── examples/               # Example usage
│   └── sample_module.py
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Running Tests

```bash
pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ for developers who value documentation
</p>
