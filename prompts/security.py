"""
Prompt criteria for Security Review mode.
Focuses on insecure patterns, injection, unsafe operations, and secrets leakage.
"""

SECURITY_REVIEW_CRITERIA = """
Perform an in-depth security analysis focusing strictly on:
1. Insecure Patterns & Injections: SQL injection, command injection, path traversal, XSS, insecure deserialization.
2. Hardcoded Secrets: Passwords, API keys, private tokens, or sensitive credentials committed directly in code.
3. Unsafe Input Handling: Absence of sanitization, missing boundary checks, or blind trust of external inputs.
4. Dangerous Operations: Unsafe dynamic evaluation (`eval`, `exec`), weak cryptography, or insecure temporary files.

Assign an overall score (1-10) reflecting the security posture of the snippet (10 = no known security flaws).
"""
