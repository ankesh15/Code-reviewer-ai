"""
Prompt criteria for Full Review mode.
Covers correctness, bugs, security vulnerabilities, code quality, and performance.
"""

FULL_REVIEW_CRITERIA = """
Perform a comprehensive, holistic code review covering:
1. Correctness & Logic: Identify edge case failures, faulty assumptions, or runtime crashes.
2. Security: Flag injection vulnerabilities, unvalidated inputs, hardcoded secrets, or unsafe operations.
3. Code Quality: Evaluate naming, readability, modularity, DRY principles, and documentation.
4. Performance & Complexity: Assess time and space complexity, spotting unnecessary bottlenecks.

Assign an overall quality score between 1 and 10 based on these combined dimensions.
"""
