# Contributing to R.A.G PDF Assistant

## 🎉 Welcome Contributors!

First off, thank you for considering contributing to R.A.G PDF Assistant! It's people like you that make this project a great tool for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code:

- **Be respectful** and inclusive
- **Be patient** and helpful to newcomers
- **Avoid** offensive or discriminatory language
- **Focus** on constructive feedback

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting bugs, include:**
- **OS and Python version**
- **Steps to reproduce**
- **Expected vs. actual behavior**
- **Error messages / screenshots**
- **Relevant configuration** (e.g., `config.py`)

**Template:**
```markdown
**Environment:**
- OS: Windows 11 / Ubuntu 22.04 / macOS 13
- Python: 3.10.5
- PyQt6: 6.4.2

**Steps to Reproduce:**
1. Load PDF with 500+ pages
2. Click "Send" button
3. Observe crash

**Expected:** Application processes PDF successfully
**Actual:** Application crashes with MemoryError

**Error Log:**
```
[Paste error traceback here]
```
```

### 💡 Suggesting Enhancements

We love new ideas! Please create an issue with:

- **Clear title** describing the feature
- **Motivation** - Why is this needed?
- **Use case** - How would you use it?
- **Implementation ideas** (optional)

---

## 🛠️ Development Setup

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/Rag-PDF-Assistant.git
cd Rag-PDF-Assistant
```

### 2. Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate

venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

pip install -r requirements-dev.txt
```

### 4. Set Up Environment

Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 5. Run Tests

```bash
pytest tests/
```

### 6. Run Application

```bash
python main.py
```

---

## 📏 Coding Standards

### Python Style Guide

We follow **PEP 8** with some extensions:

- **Line length:** 120 characters max
- **Imports:** Group standard library, third-party, and local imports
- **Type hints:** Use for function signatures where beneficial
- **Docstrings:** Use for public modules, classes, and functions

**Example:**

```python
def process_pdf(file_path: str, progress_callback=None) -> int:
    """
    Process a PDF file and extract text chunks.
    
    Args:
        file_path: Absolute path to the PDF file
        progress_callback: Optional callback for progress updates
        
    Returns:
        Number of chunks extracted
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF is corrupted
    """
    pass
```

### PyQt6 Guidelines

- **Naming:** Use `btn_` for buttons, `lbl_` for labels, `input_` for text fields
- **Signals:** Connect signals in `__init__` or dedicated setup methods
- **Threading:** Always use `QThread` for background tasks
- **Cleanup:** Properly disconnect signals and delete widgets

### Clean Code Principles

- ✅ **No debug prints** in production code
- ✅ **No commented-out code** - use version control instead
- ✅ **Minimal comments** - write self-documenting code
- ✅ **Single Responsibility** - one class/function does one thing
- ✅ **DRY** - Don't Repeat Yourself

---

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

**Examples:**

```bash
feat(ui): add dark mode toggle button

Added a toggle button in the settings menu to switch between
light and dark themes. Preference is saved to config.py.

Closes #42
```

```bash
fix(rag): prevent hallucination on empty context

Modified RAG system to return fallback message when no relevant
context is found, instead of making up information.

Resolves #87
```

```bash
docs(readme): update installation instructions

Added Windows-specific steps for installing PyQt6 dependencies.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. ✅ **Test your changes** thoroughly
2. ✅ **Update documentation** if needed
3. ✅ **Follow coding standards**
4. ✅ **Write descriptive commit messages**
5. ✅ **Ensure no debug code remains**

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested your changes.

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No console warnings
- [ ] All tests pass
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **At least one maintainer** must approve
3. **Address feedback** promptly
4. **Maintainer** will merge once approved

---

## 🧪 Testing

### Running Tests

```bash
pytest tests/ -v

pytest tests/test_rag_system.py

pytest --cov=rag_system tests/
```

### Writing Tests

Place tests in `tests/` directory:

```python
import pytest
from rag_system import RAGSystem

def test_pdf_loading():
    rag = RAGSystem()
    chunk_count = rag.process_pdf("tests/sample.pdf")
    assert chunk_count > 0

def test_empty_query():
    rag = RAGSystem()
    with pytest.raises(ValueError):
        rag.query("", "fake-api-key")
```

---

## 📚 Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [LangChain RAG Guide](https://python.langchain.com/docs/use_cases/question_answering/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [PEP 8 Style Guide](https://pep8.org/)

---

## 🙋 Questions?

- **Issues:** [GitHub Issues](https://github.com/yourusername/Rag-PDF-Assistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/Rag-PDF-Assistant/discussions)
- **Email:** your.email@example.com

---

## 🎖️ Hall of Fame

### Project Creator
**Samet YILDIZ** - Lead Developer & Project Owner  
*University Project Assignment - 2026*

### Contributors
- **Samet YILDIZ** - Core AI/ML Integration, RAG System Architecture
- **BetterCallUmut** - UI/UX Design, Audio Visualization Features

---

**Thank you for contributing! 🌟**

**Project maintained by Samet YILDIZ**
