"""
Prompt criteria for Performance Review mode.
Focuses on algorithmic efficiency, bottlenecks, redundant computations, and memory usage.
"""

PERFORMANCE_REVIEW_CRITERIA = """
Perform an algorithmic and computational performance analysis focusing strictly on:
1. Computational Complexity: Inefficient time complexity (e.g., $O(n^2)$ when $O(n)$ or $O(n \\log n)$ is achievable).
2. Memory Allocation & Footprint: Redundant data copies, unnecessary object creation, or lack of streaming/generators.
3. Unnecessary Loops & Lookups: Repeated scanning of collections ($O(n)$ list lookup) where constant-time ($O(1)$ set/hash) lookups apply.
4. I/O & Resource Inefficiencies: Repeated disk/network operations inside loops, missing batching or caching.

Assign an overall score (1-10) reflecting runtime efficiency and resource utilization.
"""
