#!/usr/bin/env python3
"""
DocForge CLI - Documentation Generator from Code
"""

import os
import sys
import click
from pathlib import Path
from typing import Optional, List
from colorama import init as colorama_init, Fore, Style

from generator import analyze_file, analyze_directory, ModuleDoc, ClassDoc, FunctionDoc

colorama_init()


def green(text: str) -> str:
    return f'{Fore.GREEN}{text}{Style.RESET_ALL}'


def blue(text: str) -> str:
    return f'{Fore.BLUE}{text}{Style.RESET_ALL}'


def yellow(text: str) -> str:
    return f'{Fore.YELLOW}{text}{Style.RESET_ALL}'


def red(text: str) -> str:
    return f'{Fore.RED}{text}{Style.RESET_ALL}'


def cyan(text: str) -> str:
    return f'{Fore.CYAN}{text}{Style.RESET_ALL}'


def format_docstring(docstring: str, indent: int = 0) -> str:
    """Format docstring for display."""
    if not docstring:
        return ''
    
    lines = docstring.strip().split('\n')
    if len(lines) == 1:
        return lines[0]
    
    return '\n' + ' ' * indent + ('\n' + ' ' * indent).join(lines)


def print_module(module: ModuleDoc, verbose: bool = False) -> None:
    """Print module documentation to console."""
    print(cyan(f'\n## Module: {module.name}'))
    print('=' * len(module.name))
    
    if module.docstring:
        print(f'\n{format_docstring(module.docstring)}\n')
    
    # Constants
    if module.constants:
        print(yellow('\nConstants:'))
        for const in module.constants:
            print(f'  - {const["name"]}: {const.get("type", "Any")}')
    
    # Classes
    if module.classes:
        print(yellow(f'\nClasses ({len(module.classes)}):'))
        for cls in module.classes:
            print_class(cls, verbose)
    
    # Functions
    if module.functions:
        print(yellow(f'\nFunctions ({len(module.functions)}):'))
        for func in module.functions:
            print_function(func, verbose)


def print_class(cls: ClassDoc, verbose: bool = False) -> None:
    """Print class documentation."""
    bases = f'({", ".join(cls.bases)})' if cls.bases else ''
    print(f'\n  {blue(f"class {cls.name}")}{bases}')
    
    if cls.docstring and verbose:
        print(f'    {format_docstring(cls.docstring, 4)}')
    
    if cls.attributes:
        for attr in cls.attributes:
            print(f'    - {attr["name"]}: {attr.get("type", "Any")}')
    
    if cls.methods:
        print(f'    {green("Methods:")}')
        for method in cls.methods:
            print(f'      {blue(method.name)}()')
            if method.docstring and verbose:
                print(f'        {format_docstring(method.docstring, 8)}')


def print_function(func: FunctionDoc, verbose: bool = False) -> None:
    """Print function documentation."""
    print(f'\n  {blue(func.signature)}')
    
    if func.docstring and verbose:
        print(f'    {format_docstring(func.docstring, 4)}')
    
    if func.returns:
        print(f'    Returns: {func.returns}')
    
    if func.raises:
        for exc in func.raises:
            print(f'    Raises: {exc}')


def generate_markdown(module: ModuleDoc, output_path: Optional[str] = None) -> str:
    """Generate Markdown documentation."""
    lines = []
    
    lines.append(f'# {module.name}')
    lines.append('')
    lines.append(f'**Path:** `{module.path}`')
    lines.append('')
    
    if module.docstring:
        lines.append(module.docstring)
        lines.append('')
    
    # Imports
    if module.imports:
        lines.append('## Imports')
        lines.append('')
        lines.append('```python')
        for imp in module.imports[:20]:  # Limit imports in docs
            lines.append(f'import {imp}')
        if len(module.imports) > 20:
            lines.append(f'# ... and {len(module.imports) - 20} more')
        lines.append('```')
        lines.append('')
    
    # Constants
    if module.constants:
        lines.append('## Constants')
        lines.append('')
        for const in module.constants:
            lines.append(f'- `{const["name"]}`: {const.get("type", "Any")}')
        lines.append('')
    
    # Classes
    if module.classes:
        lines.append('## Classes')
        lines.append('')
        
        for cls in module.classes:
            bases = f'({", ".join(cls.bases)})' if cls.bases else ''
            lines.append(f'### `{cls.name}`')
            lines.append('')
            lines.append(f'*Inherits from: {bases}*' if bases else '')
            
            if cls.docstring:
                lines.append('')
                lines.append(cls.docstring)
            
            if cls.decorators:
                lines.append('')
                for dec in cls.decorators:
                    lines.append(f'`{dec}`')
            
            if cls.attributes:
                lines.append('')
                lines.append('**Attributes:**')
                lines.append('')
                for attr in cls.attributes:
                    lines.append(f'- `{attr["name"]}`: {attr.get("type", "Any")}')
                    if attr.get('description'):
                        lines.append(f'  {attr["description"]}')
            
            if cls.methods:
                lines.append('')
                lines.append('**Methods:**')
                lines.append('')
                for method in cls.methods:
                    lines.append(f'#### `{method.name}`')
                    lines.append('')
                    lines.append(f'```python')
                    lines.append(f'{method.signature}')
                    lines.append(f'```')
                    lines.append('')
                    
                    if method.docstring:
                        lines.append(method.docstring)
                        lines.append('')
                    
                    if method.parameters:
                        lines.append('**Parameters:**')
                        lines.append('')
                        for param in method.parameters:
                            lines.append(f'- `{param["name"]}` ({param.get("type", "Any")}): {param.get("description", "")}')
                        lines.append('')
                    
                    if method.returns:
                        lines.append(f'**Returns:** {method.returns}')
                        lines.append('')
                    
                    if method.raises:
                        lines.append('**Raises:**')
                        for exc in method.raises:
                            lines.append(f'- {exc}')
                        lines.append('')
    
    # Functions
    if module.functions:
        lines.append('## Functions')
        lines.append('')
        
        for func in module.functions:
            lines.append(f'### `{func.name}`')
            lines.append('')
            lines.append(f'```python')
            lines.append(func.signature)
            lines.append(f'```')
            lines.append('')
            
            if func.docstring:
                lines.append(func.docstring)
                lines.append('')
            
            if func.parameters:
                lines.append('**Parameters:**')
                lines.append('')
                for param in func.parameters:
                    lines.append(f'- `{param["name"]}` ({param.get("type", "Any")}): {param.get("description", "")}')
                lines.append('')
            
            if func.returns:
                lines.append(f'**Returns:** {func.returns}')
                lines.append('')
            
            if func.raises:
                lines.append('**Raises:**')
                for exc in func.raises:
                    lines.append(f'- {exc}')
                lines.append('')
    
    output = '\n'.join(lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        click.echo(green(f'Documentation written to: {output_path}'))
    
    return output


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """DocForge - Generate documentation from Python source code."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--format', '-f', type=click.Choice(['markdown', 'console']), default='console', help='Output format')
def generate(path: str, output: Optional[str], verbose: bool, format: str):
    """Generate documentation for a Python file or directory."""
    
    path_obj = Path(path)
    
    if path_obj.is_file():
        if not path.endswith('.py'):
            click.echo(red('Error: Only Python files are supported'))
            sys.exit(1)
        
        click.echo(green(f'Analyzing: {path}'))
        module = analyze_file(path)
        modules = [module]
    else:
        click.echo(green(f'Analyzing directory: {path}'))
        modules = analyze_directory(path)
        click.echo(f'Found {len(modules)} module(s)')
    
    if format == 'console':
        for module in modules:
            print_module(module, verbose)
    else:
        # Generate markdown
        if len(modules) == 1:
            output_path = output or f'{modules[0].name}_docs.md'
            generate_markdown(modules[0], output_path)
        else:
            # Multiple modules - create index and individual files
            if output:
                click.echo(red('Error: Use --output with a single file'))
                sys.exit(1)
            
            output_dir = Path('docs')
            output_dir.mkdir(exist_ok=True)
            
            # Create index
            index_lines = ['# Documentation Index\n']
            for module in modules:
                index_lines.append(f'- [{module.name}]({module.name}.md)')
            index_lines.append('')
            
            with open(output_dir / 'README.md', 'w') as f:
                f.write('\n'.join(index_lines))
            
            # Generate each module
            for module in modules:
                generate_markdown(module, str(output_dir / f'{module.name}.md'))


@cli.command()
@click.argument('path', type=click.Path(exists=True))
def analyze(path: str):
    """Analyze Python code and show statistics."""
    
    path_obj = Path(path)
    
    if path_obj.is_file():
        module = analyze_file(path)
        modules = [module]
    else:
        modules = analyze_directory(path)
    
    total_classes = sum(len(m.classes) for m in modules)
    total_functions = sum(len(m.functions) for m in modules)
    total_methods = sum(
        sum(len(c.methods) for c in m.classes)
        for m in modules
    )
    
    click.echo(cyan('\n📊 Analysis Results'))
    click.echo('=' * 40)
    click.echo(f'Modules:   {green(str(len(modules)))}')
    click.echo(f'Classes:   {green(str(total_classes))}')
    click.echo(f'Functions: {green(str(total_functions))}')
    click.echo(f'Methods:   {green(str(total_methods))}')
    click.echo('')


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), default='README.md', help='Output file')
def init(path: str, output: str):
    """Initialize documentation for a project."""
    
    click.echo(cyan(f'Initializing documentation for: {path}'))
    
    modules = analyze_directory(path)
    
    if not modules:
        click.echo(red('No Python modules found'))
        sys.exit(1)
    
    # Generate main README
    lines = [
        f'# {Path(path).name}',
        '',
        '## Table of Contents',
        ''
    ]
    
    for module in modules:
        lines.append(f'- [{module.name}](#{module.name.lower().replace(".", "-")})')
    
    lines.extend(['', '## Modules', ''])
    
    for module in modules:
        lines.append(f'### {module.name}')
        lines.append('')
        
        if module.docstring:
            lines.append(module.docstring)
        else:
            lines.append(f'*No module documentation*')
        
        lines.append('')
        
        if module.classes:
            lines.append(f'**Classes:** {", ".join(c.name for c in module.classes)}')
            lines.append('')
        
        if module.functions:
            lines.append(f'**Functions:** {", ".join(f.name for f in module.functions)}')
            lines.append('')
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    click.echo(green(f'Documentation initialized: {output}'))


if __name__ == '__main__':
    cli()
