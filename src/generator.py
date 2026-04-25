#!/usr/bin/env python3
"""
DocForge - Documentation Generator
Automatically generates documentation from Python source code.
"""

import os
import re
import ast
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FunctionDoc:
    """Documentation for a function/method."""
    name: str
    signature: str
    docstring: str
    decorators: List[str] = field(default_factory=list)
    parameters: List[Dict[str, str]] = field(default_factory=list)
    returns: Optional[str] = None
    raises: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)


@dataclass
class ClassDoc:
    """Documentation for a class."""
    name: str
    docstring: str
    bases: List[str] = field(default_factory=list)
    methods: List[FunctionDoc] = field(default_factory=list)
    attributes: List[Dict[str, str]] = field(default_factory=list)
    decorators: List[str] = field(default_factory=list)


@dataclass
class ModuleDoc:
    """Documentation for a module."""
    name: str
    path: str
    docstring: str
    classes: List[ClassDoc] = field(default_factory=list)
    functions: List[FunctionDoc] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    constants: List[Dict[str, str]] = field(default_factory=list)


class DocstringParser:
    """Parses docstrings into structured components."""
    
    @staticmethod
    def parse(docstring: str) -> Dict[str, Any]:
        """Parse a docstring into sections."""
        if not docstring:
            return {'description': '', 'params': [], 'returns': None, 'raises': [], 'examples': []}
        
        sections = {
            'description': '',
            'params': [],
            'returns': None,
            'raises': [],
            'examples': []
        }
        
        if not docstring:
            return sections
        
        # Split into lines
        lines = docstring.strip().split('\n')
        
        current_section = 'description'
        current_param = None
        param_description_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Check for section headers
            if stripped.startswith('Args:') or stripped.startswith('Arguments:'):
                current_section = 'params'
                continue
            elif stripped.startswith('Returns:') or stripped.startswith('Return:'):
                current_section = 'returns'
                continue
            elif stripped.startswith('Raises:'):
                current_section = 'raises'
                continue
            elif stripped.startswith('Example:') or stripped.startswith('Examples:'):
                current_section = 'examples'
                continue
            
            # Handle description section
            if current_section == 'description':
                if sections['description'] and stripped:
                    sections['description'] += '\n' + stripped
                elif stripped:
                    sections['description'] = stripped
            
            # Handle params
            elif current_section == 'params':
                # Check for new param
                param_match = re.match(r'(\w+):\s*(.*)', stripped)
                if param_match:
                    if current_param:
                        sections['params'].append({
                            'name': current_param,
                            'description': ' '.join(param_description_lines)
                        })
                    current_param = param_match.group(1)
                    param_description_lines = [param_match.group(2)]
                elif stripped and current_param:
                    param_description_lines.append(stripped)
            
            # Handle returns
            elif current_section == 'returns':
                if sections['returns'] is None:
                    sections['returns'] = stripped
                elif stripped:
                    sections['returns'] += ' ' + stripped
            
            # Handle raises
            elif current_section == 'raises':
                if stripped:
                    sections['raises'].append(stripped)
            
            # Handle examples
            elif current_section == 'examples':
                if stripped:
                    sections['examples'].append(stripped)
        
        # Close last param
        if current_param and current_section == 'params':
            sections['params'].append({
                'name': current_param,
                'description': ' '.join(param_description_lines)
            })
        
        return sections


class PythonCodeAnalyzer(ast.NodeVisitor):
    """Analyzes Python source code using AST."""
    
    def __init__(self):
        self.modules: List[ModuleDoc] = []
        self.current_module: Optional[ModuleDoc] = None
        self.current_class: Optional[ClassDoc] = None
        self.docstring_parser = DocstringParser()
    
    def visit_Module(self, node: ast.Module) -> None:
        """Visit a module node."""
        docstring = ast.get_docstring(node) or ''
        self.current_module = ModuleDoc(
            name=Path(self.modules[-1].path if self.modules else 'unknown').stem,
            path='',
            docstring=docstring
        )
        
        # Collect imports
        for item in node.body:
            if isinstance(item, ast.Import):
                for alias in item.names:
                    self.current_module.imports.append(alias.name)
            elif isinstance(item, ast.ImportFrom):
                module_name = item.module or ''
                for alias in item.names:
                    self.current_module.imports.append(f'{module_name}.{alias.name}')
        
        # Visit all items
        self.generic_visit(node)
        
        if self.current_module:
            self.modules.append(self.current_module)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition."""
        # Get base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(self._get_attribute_name(base))
        
        # Get decorators
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        # Get docstring
        docstring = ast.get_docstring(node) or ''
        
        # Get class attributes
        attributes = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                type_hint = self._get_type_hint(item.annotation)
                attributes.append({
                    'name': item.target.id,
                    'type': type_hint
                })
        
        # Create class doc
        class_doc = ClassDoc(
            name=node.name,
            docstring=docstring,
            bases=bases,
            attributes=attributes,
            decorators=decorators
        )
        
        # Parse docstring sections
        if docstring:
            parsed = self.docstring_parser.parse(docstring)
            class_doc.attributes.extend([
                {'name': p['name'], 'type': 'param', 'description': p['description']}
                for p in parsed['params']
            ])
        
        # Save current class and process
        old_class = self.current_class
        self.current_class = class_doc
        
        # Visit methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
                self.visit_FunctionDef(item)
        
        # Restore class
        self.current_class = old_class
        
        if self.current_module:
            self.current_module.classes.append(class_doc)
    
    def visit_FunctionDef(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        """Visit a function definition."""
        # Skip private functions if configured
        if node.name.startswith('_') and not node.name.startswith('__'):
            return
        
        # Get decorators
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]
        
        # Get signature
        signature = self._get_signature(node)
        
        # Get docstring
        docstring = ast.get_docstring(node) or ''
        
        # Parse parameters
        parameters = []
        for arg in node.args.args:
            parameters.append({
                'name': arg.arg,
                'type': self._get_type_hint(arg.annotation) if arg.annotation else 'Any'
            })
        
        # Get return type
        returns = None
        if node.returns:
            returns = self._get_type_hint(node.returns)
        
        # Create function doc
        func_doc = FunctionDoc(
            name=node.name,
            signature=signature,
            docstring=docstring,
            decorators=decorators,
            parameters=parameters,
            returns=returns
        )
        
        # Parse docstring sections
        if docstring:
            parsed = self.docstring_parser.parse(docstring)
            func_doc.returns = parsed['returns']
            func_doc.raises = parsed['raises']
            func_doc.examples = parsed['examples']
        
        if self.current_class:
            self.current_class.methods.append(func_doc)
        elif self.current_module:
            self.current_module.functions.append(func_doc)
    
    def _get_signature(self, node: ast.FunctionDef) -> str:
        """Get function signature as string."""
        args = node.args
        
        # Get argument names
        arg_names = []
        for i, arg in enumerate(args.args):
            arg_name = arg.arg
            if arg.annotation:
                arg_name += f': {self._get_type_hint(arg.annotation)}'
            arg_names.append(arg_name)
        
        # Add *args and **kwargs
        if args.vararg:
            vararg = f'*{args.vararg.arg}'
            if args.vararg.annotation:
                vararg += f': {self._get_type_hint(args.vararg.annotation)}'
            arg_names.append(vararg)
        
        if args.kwarg:
            kwarg = f'**{args.kwarg.arg}'
            if args.kwarg.annotation:
                kwarg += f': {self._get_type_hint(args.kwarg.annotation)}'
            arg_names.append(kwarg)
        
        return f'{node.name}({", ".join(arg_names)})'
    
    def _get_type_hint(self, node: Optional[ast.AST]) -> str:
        """Convert type hint AST to string."""
        if node is None:
            return 'Any'
        
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f'{self._get_type_hint(node.value)}.{node.attr}'
        elif isinstance(node, ast.Subscript):
            base = self._get_type_hint(node.value)
            if isinstance(node.slice, ast.Tuple):
                args = ', '.join(self._get_type_hint(e) for e in node.slice.elts)
                return f'{base}[{args}]'
            else:
                return f'{base}[{self._get_type_hint(node.slice)}]'
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.BinOp):
            return f'{self._get_type_hint(node.left)} | {self._get_type_hint(node.right)}'
        else:
            return str(type(node).__name__)
    
    def _get_decorator_name(self, node: ast.AST) -> str:
        """Get decorator name as string."""
        if isinstance(node, ast.Name):
            return f'@{node.id}'
        elif isinstance(node, ast.Attribute):
            return f'@{self._get_type_hint(node)}'
        elif isinstance(node, ast.Call):
            return f'{self._get_decorator_name(node.func)}'
        return '@decorator'
    
    def _get_attribute_name(self, node: ast.Attribute) -> str:
        """Get attribute name chain."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f'{self._get_attribute_name(node.value)}.{node.attr}'
        return 'Unknown'


def analyze_file(filepath: str) -> ModuleDoc:
    """Analyze a Python file and extract documentation."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    analyzer = PythonCodeAnalyzer()
    analyzer.current_module = ModuleDoc(
        name=Path(filepath).stem,
        path=filepath,
        docstring=''
    )
    analyzer.visit(tree)
    
    if analyzer.current_module:
        analyzer.current_module.path = filepath
        return analyzer.current_module
    
    return ModuleDoc(name=Path(filepath).stem, path=filepath, docstring='')


def analyze_directory(dirpath: str, pattern: str = '*.py') -> List[ModuleDoc]:
    """Analyze all Python files in a directory."""
    modules = []
    path = Path(dirpath)
    
    for filepath in path.rglob(pattern):
        # Skip __pycache__ and test files
        if '__pycache__' in str(filepath) or 'test_' in filepath.name:
            continue
        
        try:
            module = analyze_file(str(filepath))
            modules.append(module)
        except Exception as e:
            print(f'Warning: Could not analyze {filepath}: {e}')
    
    return modules
