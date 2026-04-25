# DocForge

<p align="center">
  <img src="https://img.shields.io/badge/Docs-Auto-FF6B6B?style=for-the-badge&logo=book&logoColor=white" alt="Docs">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

> 📖 **Auto-Generated Documentation** - Generates documentation from code, tests, and commits. Maintains docs as code evolves.

## ✨ Features

### Documentation Types
- 📄 **API Docs** - Endpoints, parameters, examples
- 📦 **SDK Docs** - Libraries, packages, modules
- 🏗️ **Architecture** - System design, diagrams
- 📖 **Guides** - Tutorials, how-tos
- 📋 **Reference** - Type definitions, schemas

### Generation Sources
- 💻 **Code Analysis** - AST parsing, type inference
- 🧪 **Tests** - Extract examples from tests
- 📝 **Commits** - Track changes over time
- 🗒️ **Comments** - Inline documentation
- 🏷️ **Annotations** - JSDoc, docstrings

### Output Formats
- 🌐 **Markdown** - GitHub/GitLab compatible
- 📘 **OpenAPI** - Swagger documentation
- 📑 **HTML** - Static site generation
- 📱 **Docusaurus** - Export to Docusaurus
- 📖 **MkDocs** - MkDocs compatible

## 📦 Installation

```bash
git clone https://github.com/moggan1337/DocForge.git
cd DocForge
pip install -r requirements.txt
docforge init
```

## 🚀 Usage

```bash
# Generate docs for a project
docforge generate ./my-project

# Watch mode - regenerate on changes
docforge watch ./my-project

# Serve locally
docforge serve ./docs
```

## 📄 License

MIT License
