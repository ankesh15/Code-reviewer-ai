"""
Prompt factory and registry for AI Code Reviewer.
Combines system persona, specialized review criteria, domain guidelines context,
and structured JSON output constraints.
Supports both all-in-one comprehensive reviews with automatic language detection
and specialized single-mode reviews.
"""

from typing import Dict, Optional
from .review import FULL_REVIEW_CRITERIA
from .bugs import BUG_DETECTION_CRITERIA
from .security import SECURITY_REVIEW_CRITERIA
from .quality import CODE_QUALITY_CRITERIA
from .performance import PERFORMANCE_REVIEW_CRITERIA

SYSTEM_PERSONA = (
    "You are an experienced senior software engineer performing a rigorous, constructive, "
    "and actionable code review across all major programming languages (Python, JavaScript, "
    "TypeScript, C++, Java, C, Go, Rust, etc.)."
)

REVIEW_MODES: Dict[str, Dict[str, str]] = {
    "Full Review": {
        "title": "Full Comprehensive Review",
        "description": "Examines correctness, security, code quality, and performance holistically.",
        "criteria": FULL_REVIEW_CRITERIA,
    },
    "Bug Detection": {
        "title": "Bug & Defect Detection",
        "description": "Pinpoints logic bugs, edge cases, off-by-one errors, and unhandled exceptions.",
        "criteria": BUG_DETECTION_CRITERIA,
    },
    "Security Review": {
        "title": "Security & Vulnerability Analysis",
        "description": "Identifies injection risks, hardcoded credentials, unsafe input handling, and risky operations.",
        "criteria": SECURITY_REVIEW_CRITERIA,
    },
    "Code Quality": {
        "title": "Code Quality & Maintainability",
        "description": "Evaluates readability, naming, adherence to idiomatic conventions, DRY, and modularity.",
        "criteria": CODE_QUALITY_CRITERIA,
    },
    "Performance Review": {
        "title": "Performance & Complexity Analysis",
        "description": "Identifies algorithmic bottlenecks, high time/space complexity, and unnecessary overhead.",
        "criteria": PERFORMANCE_REVIEW_CRITERIA,
    },
}

COMPREHENSIVE_SCHEMA_INSTRUCTIONS = """
You MUST return your review strictly as a valid JSON object. Do not include markdown code fences (```json) outside the JSON.
Follow this exact JSON structure:
{
  "detected_language": "<Programming language detected, e.g. Python, C++, JavaScript, TypeScript, Java, C, Go, etc.>",
  "overall_score": <integer from 1 to 10>,
  "summary": "<Concise 2-3 sentence overview of the code's quality, main strengths, and key concerns>",
  "issues": [
    {
      "severity": "<HIGH | MEDIUM | LOW>",
      "category": "<BUG | SECURITY | PERFORMANCE | QUALITY>",
      "line": <integer line number or null if general/cannot be determined accurately>,
      "problem": "<Short 1-sentence title of the issue>",
      "explanation": "<Clear technical explanation of why this is problematic>",
      "suggested_fix": "<Concise code snippet or instruction on how to resolve it>"
    }
  ],
  "suggestions": [
    "<Actionable recommendation 1>",
    "<Actionable recommendation 2>"
  ],
  "complexity": {
    "time": "<Big-O time complexity estimate, e.g. O(1), O(n), O(n log n), O(n^2), or 'N/A'>",
    "space": "<Big-O space complexity estimate, e.g. O(1), O(n), or 'N/A'>"
  },
  "fixed_code": "<The complete, improved and refactored code snippet implementing all fixes and best practices>"
}

Review Instructions:
1. Automatically identify the programming language from the code syntax.
2. Evaluate all 4 core pillars:
   - BUG: Identify logical bugs, boundary/edge conditions, off-by-one errors, null pointer/unhandled exceptions.
   - SECURITY: Identify injections, hardcoded secrets, buffer overflow risks, unsafe dynamic operations, unvalidated inputs.
   - PERFORMANCE: Identify inefficient algorithms, redundant loops/lookups, unnecessary memory allocations.
   - QUALITY: Evaluate readability, naming, clean-code principles, maintainability, DRY, and language idioms.
3. Determine Big-O time and space complexity.
4. Provide concrete, actionable recommendations.
5. Provide complete, working, improved/fixed code.
6. Only provide line numbers if accurately identifiable from the snippet; otherwise use null. Never fabricate line numbers.
7. Return strictly valid JSON.
"""


def build_comprehensive_prompt(code: str, guidelines: str = "") -> str:
    """
    Constructs a unified, comprehensive review prompt with automatic language detection,
    all review pillars (Bugs, Security, Performance, Quality), complexity analysis, and fixed code.
    """
    prompt_parts = [
        f"ROLE: {SYSTEM_PERSONA}",
        "\nTASK: Automatically detect the programming language and perform a comprehensive, 360-degree code analysis covering Bugs, Security, Performance, Code Quality, and Algorithmic Complexity.",
    ]

    if guidelines:
        prompt_parts.append(
            f"\n=== ENGINEERING GUIDELINES & BEST PRACTICES ===\n{guidelines.strip()}"
        )

    prompt_parts.append(
        f"\n=== CODE TO REVIEW ===\n"
        f"```\n"
        f"{code}\n"
        f"```"
    )

    prompt_parts.append(f"\n=== OUTPUT FORMAT INSTRUCTIONS ===\n{COMPREHENSIVE_SCHEMA_INSTRUCTIONS.strip()}")

    return "\n".join(prompt_parts)


def build_prompt(code: str, language: str, mode: str, guidelines: str = "") -> str:
    """
    Constructs a specialized review prompt for a specific mode and language.
    Retained for targeted evaluation and backward compatibility.
    """
    mode_config = REVIEW_MODES.get(mode, REVIEW_MODES["Full Review"])
    criteria = mode_config["criteria"]

    prompt_parts = [
        f"ROLE: {SYSTEM_PERSONA}",
        f"\nTARGET PROGRAMMING LANGUAGE: {language}",
        f"REVIEW MODE: {mode} ({mode_config['title']})",
        f"\n=== REVIEW CRITERIA ===\n{criteria.strip()}",
    ]

    if guidelines:
        prompt_parts.append(
            f"\n=== ENGINEERING GUIDELINES & BEST PRACTICES ({language}) ===\n"
            f"Use these team guidelines to assess the code:\n{guidelines.strip()}"
        )

    prompt_parts.append(
        f"\n=== CODE TO REVIEW ===\n"
        f"```{language.lower()}\n"
        f"{code}\n"
        f"```"
    )

    prompt_parts.append(f"\n=== OUTPUT FORMAT INSTRUCTIONS ===\n{COMPREHENSIVE_SCHEMA_INSTRUCTIONS.strip()}")

    return "\n".join(prompt_parts)
