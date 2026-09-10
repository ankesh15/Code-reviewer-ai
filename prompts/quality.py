"""
Prompt criteria for Code Quality mode.
Focuses on readability, maintainability, naming, duplication, and structure.
"""

CODE_QUALITY_CRITERIA = """
Perform an extensive code quality and clean code review focusing strictly on:
1. Readability & Idioms: Adherence to language conventions (PEP 8 for Python, ES6+ for JavaScript), clear structure.
2. Maintainability & Modularity: Single responsibility principle, appropriate function length, avoidance of monolithic blocks.
3. Naming Conventions: Descriptive variable, function, and parameter names avoiding cryptic single-letter abbreviations.
4. Duplication & DRY: Redundant logic, copy-pasted blocks, or patterns better abstracted into helper utilities.
5. Documentation & Typing: Clarity of comments, type annotations, and docstrings explaining non-obvious intent.

Assign an overall score (1-10) evaluating the cleanliness, readability, and long-term maintainability.
"""
