"""
Prompt criteria for Bug Detection mode.
Focuses on logical errors, edge cases, incorrect assumptions, and runtime issues.
"""

BUG_DETECTION_CRITERIA = """
Perform a deep-dive bug and defect analysis focusing strictly on:
1. Logical Errors: Incorrect branching, flawed loop conditions, off-by-one indices, broken math.
2. Edge Cases & Boundary Values: Empty collections, null/None inputs, zero-division, type mismatches.
3. Unhandled Exceptions: Operations susceptible to uncaught exceptions, missing error handling.
4. Faulty Assumptions: Invalidation of state invariants or improper handling of mutable variables.

Assign an overall score (1-10) reflecting code correctness and robustness against defects.
"""
