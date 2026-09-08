# Instructions for GitHub Copilot

## General Coding Guidelines
- Follow **PEP 8** for Python code style and formatting.
- Use **type hints** wherever applicable to improve code readability and maintainability.
- Ensure all code is modular and reusable.
- Use OOP principles where applicable, especially for complex components.
- Try to re-use existing code where it makes sense.
- Follow the DRY principle - don't repeat yourself.
- Add meaningful log statements where it makes sense (INFO, WARNING, ERROR, DEBUG).
- When asked to create a standalone package, use `cx_freeze`

## Python Environment Rules
- Always use `uv` for package management, Python environment creation and Python execution.
- Ensure all dependencies are listed in pyproject.toml.

## Testing Guidelines
- Do just enough testing to ensure the basic functionality works.
- Do not use mocking.

## Additional Notes
- Properly handle sensitive information (e.g., API keys, database credentials).
- Update/Create README.md when necessary.
- Always use forward slash file separators ("/") in paths.