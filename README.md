# DocForge 📝

Auto-generate beautiful documentation from Python source code using AST analysis.

## Features

- **AST-Based Analysis**: Parses Python code using the Abstract Syntax Tree
- **Smart Docstring Parsing**: Extracts Args, Returns, Raises, Examples sections
- **Multiple Output Formats**: Console, Markdown
- **Type Hints Support**: Preserves type annotations in documentation
- **Decorator Tracking**: Documents decorators on functions and classes
- **Project Analysis**: Analyze entire directories

## Installation

```bash
pip install -r requirements.txt
```

Or install locally:

```bash
pip install click jinja2 markdown astor colorama
```

## Usage

### Generate documentation for a file

```bash
python src/cli.py generate path/to/module.py
```

### Generate documentation for a directory

```bash
python src/cli.py generate path/to/project
```

### Generate Markdown output

```bash
python src/cli.py generate path/to/module.py --format markdown -o docs.md
```

### Analyze code statistics

```bash
python src/cli.py analyze path/to/project
```

### Initialize project documentation

```bash
python src/cli.py init path/to/project
```

## Examples

### Console Output

```bash
$ python src/cli.py generate my_module.py --verbose

## Module: my_module
========================

### Classes (1):

  class MyClass
    - attribute1: str

    Methods:
      method1()

## Functions (1):

  def process_data(input: str, options: Dict) -> bool
```

### Markdown Output

Generates well-structured Markdown with:
- Module overview
- Class documentation with inheritance
- Method signatures and docstrings
- Parameter documentation
- Return types
- Raises sections

## Command Options

- `generate` - Generate documentation
  - `--output, -o` - Output file path
  - `--verbose, -v` - Verbose output
  - `--format, -f` - Output format (console/markdown)

- `analyze` - Show code statistics

- `init` - Initialize project documentation

## Docstring Format

DocForge supports Google-style and NumPy-style docstrings:

```python
def process_data(input: str, count: int = 10) -> bool:
    """Process input data.

    Args:
        input: The input string to process
        count: Number of iterations (default: 10)

    Returns:
        True if successful, False otherwise

    Raises:
        ValueError: If input is empty

    Example:
        >>> process_data("hello", 5)
        True
    """
    pass
```

## Architecture

```
src/
├── cli.py          # Click CLI interface
└── generator.py    # AST code analysis
```

## License

MIT
