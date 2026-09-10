# Python Engineering & Review Guidelines

## 1. Code Style & Readability
- Follow **PEP 8** conventions: `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Include Python type annotations (`typing`) on function arguments and return types for clarity.
- Keep functions concise with a single, clear responsibility (Single Responsibility Principle).

## 2. Common Bug Prevention & Edge Cases
- **Mutable Default Arguments**: Never use mutable objects (like `[]` or `{}`) as default function arguments. Use `None` and initialize inside the function.
- **Exception Handling**: Avoid bare `except:`. Always catch specific exceptions (e.g., `ValueError`, `KeyError`) and preserve traceback context.
- **Null Safety**: Explicitly check for `None` before attribute access or iteration.
- **Resource Management**: Always use `with` statements (context managers) for file, network, and database operations to guarantee cleanup.

## 3. Security Best Practices
- **Injection Prevention**: Never concatenate raw user input into SQL queries or shell commands. Use parameterized queries or ORM methods.
- **Dynamic Execution**: Strictly avoid `eval()`, `exec()`, or `pickle.loads()` on untrusted input.
- **Secrets Management**: Never commit hardcoded API keys, passwords, or tokens. Load secrets via environment variables (`os.getenv`).
- **Input Validation**: Validate boundaries, data types, and sanitize incoming payload data before processing.

## 4. Performance & Algorithmic Efficiency
- **Lookup Complexity**: Use `set` or `dict` for membership testing ($O(1)$ average) instead of `list` ($O(n)$).
- **Nested Loops**: Flag quadratic $O(n^2)$ or higher nested loops that can be simplified using hashing or batching.
- **String Concatenation**: Avoid repeated `+=` string concatenation inside loops; use `''.join()` or list accumulation.
- **Generators**: Use generator expressions or `yield` when streaming large datasets to prevent unbounded memory usage.
