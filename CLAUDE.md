# DocForge

Documentation generator that parses Python source code using AST.

## Tech Stack

- **Language**: Python 3
- **CLI Framework**: Click
- **Code Analysis**: ast (standard library)
- **Formatting**: colorama, markdown

## Key Files

- `src/cli.py` - Click CLI interface with commands
- `src/generator.py` - AST analyzer and documentation generator

## CLI Commands

1. `generate` - Main command to generate documentation
2. `analyze` - Show statistics about code
3. `init` - Initialize project documentation

## Generator Classes

- `PythonCodeAnalyzer` - AST visitor that extracts code structure
- `DocstringParser` - Parses docstrings into sections (Args, Returns, Raises)
- `ModuleDoc`, `ClassDoc`, `FunctionDoc` - Documentation data classes

## Supported Features

- Function signatures with type hints
- Class inheritance
- Decorators
- Docstring sections (Args, Returns, Raises, Examples)
- Google-style and NumPy-style docstrings
- Module-level constants

## Output Formats

- Console (colored text output)
- Markdown (full documentation)

## Usage

```bash
# Generate docs for a file
python src/cli.py generate module.py

# Generate Markdown docs
python src/cli.py generate module.py -f markdown -o docs.md

# Analyze code stats
python src/cli.py analyze module.py
```

## Extending

- Add new output formats (HTML, PDF via Jinja2 templates)
- Add support for other languages (JavaScript, TypeScript)
- Add documentation linting
- Add template customization
