"""
Helper utilities for guideline loading, robust JSON response sanitization,
and preset sample code snippets for interactive review.
"""

import json
import os
import re
from typing import Any, Dict, Optional

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDELINES_DIR = os.path.join(BASE_DIR, "guidelines")


def load_guidelines(language: str = "") -> str:
    """
    Loads markdown guidelines for the specified programming language,
    or a composite multi-language engineering guideline if language is not explicitly provided.
    """
    normalized_lang = language.strip().lower() if language else ""
    file_map = {
        "python": "python.md",
        "javascript": "javascript.md",
        "js": "javascript.md",
        "typescript": "javascript.md",
        "ts": "javascript.md",
    }

    if normalized_lang in file_map:
        filepath = os.path.join(GUIDELINES_DIR, file_map[normalized_lang])
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except IOError:
                pass

    # If general or auto-detected, provide composite guidelines for context
    combined = []
    for fname in ["python.md", "javascript.md"]:
        fpath = os.path.join(GUIDELINES_DIR, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    combined.append(f.read().strip())
            except IOError:
                pass
    return "\n\n".join(combined)


def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """
    Robustly extracts and parses a JSON object from LLM response text.
    Handles markdown wrappers, whitespace, and falls back gracefully on errors.
    """
    cleaned = raw_text.strip()

    # 1. Try stripping markdown code fences if wrapped in ```json ... ```
    if cleaned.startswith("```"):
        # Strip opening ```json or ```
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        # Strip closing ```
        cleaned = re.sub(r"\n?```$", "", cleaned)
        cleaned = cleaned.strip()

    # 2. Try direct json.loads
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return _normalize_review_data(data)
    except json.JSONDecodeError:
        pass

    # 3. Try regex extraction of the outermost JSON object {...}
    json_match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            if isinstance(data, dict):
                return _normalize_review_data(data)
        except json.JSONDecodeError:
            pass

    # 4. Fallback if JSON parsing completely fails: never crash the app
    return {
        "detected_language": "Auto-Detected",
        "overall_score": 5,
        "summary": raw_text[:300] + "..." if len(raw_text) > 300 else raw_text,
        "issues": [
            {
                "severity": "MEDIUM",
                "category": "QUALITY",
                "line": None,
                "problem": "Output Parsing Fallback",
                "explanation": "The model response could not be parsed as strict JSON. Displaying raw output.",
                "suggested_fix": "Please retry analysis or check prompt configuration."
            }
        ],
        "suggestions": ["Review the raw model output for findings."],
        "complexity": {"time": "N/A", "space": "N/A"},
        "fixed_code": raw_text,
        "_raw_fallback": True,
    }


def _normalize_review_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures that parsed JSON contains all expected keys with appropriate defaults.
    """
    # Detected language normalization
    detected_lang = str(data.get("detected_language", "Auto-Detected")).strip()
    if not detected_lang or detected_lang.lower() in ("null", "none", "unknown"):
        detected_lang = "Auto-Detected"

    # Score normalization (clamp between 1 and 10)
    score = data.get("overall_score", 5)
    try:
        score = int(score)
        score = max(1, min(10, score))
    except (ValueError, TypeError):
        score = 5

    # Issues normalization
    raw_issues = data.get("issues", [])
    normalized_issues = []
    if isinstance(raw_issues, list):
        for item in raw_issues:
            if isinstance(item, dict):
                severity = str(item.get("severity", "MEDIUM")).upper()
                if severity not in ("HIGH", "MEDIUM", "LOW"):
                    severity = "MEDIUM"

                category = str(item.get("category", "QUALITY")).upper()
                if category not in ("BUG", "SECURITY", "QUALITY", "PERFORMANCE"):
                    category = "QUALITY"

                line = item.get("line")
                try:
                    line = int(line) if line is not None else None
                except (ValueError, TypeError):
                    line = None

                normalized_issues.append({
                    "severity": severity,
                    "category": category,
                    "line": line,
                    "problem": str(item.get("problem", "Unspecified Issue")),
                    "explanation": str(item.get("explanation", "")),
                    "suggested_fix": str(item.get("suggested_fix", "")),
                })

    # Complexity normalization
    comp = data.get("complexity", {})
    if not isinstance(comp, dict):
        comp = {}
    normalized_complexity = {
        "time": str(comp.get("time", "N/A")),
        "space": str(comp.get("space", "N/A")),
    }

    return {
        "detected_language": detected_lang,
        "overall_score": score,
        "summary": str(data.get("summary", "No summary provided.")),
        "issues": normalized_issues,
        "suggestions": [str(s) for s in data.get("suggestions", []) if isinstance(s, (str, int))],
        "complexity": normalized_complexity,
        "fixed_code": str(data.get("fixed_code", "")),
    }


# Preset sample code snippets for quick testing
SAMPLE_CODE_SNIPPETS = {
    "Python": {
        "SQL Injection & Insecure Auth": '''import sqlite3

def login_user(username, password):
    # Security risk: String formatting permits SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user
''',
        "Inefficient Quadratic Nested Loop": '''def find_common_elements(list_a, list_b):
    # Inefficient O(n*m) complexity using nested scan
    common = []
    for item_a in list_a:
        for item_b in list_b:
            if item_a == item_b and item_a not in common:
                common.append(item_a)
    return common
''',
        "Mutable Default & Bare Except": '''def append_event(event_name, event_list=[]):
    # Bug: Mutable default argument retains state across invocations
    try:
        event_list.append(event_name)
        with open("events.log", "a") as f:
            f.write(event_name + "\\n")
        return event_list
    except:
        # Quality issue: Bare except silently suppresses all exceptions
        print("An error occurred")
''',
    },
    "JavaScript": {
        "Insecure Eval & DOM Injection": '''function renderUserContent(userInput) {
    // Security risk: eval execution and unescaped HTML injection
    eval("var computed = " + userInput);
    document.getElementById("output").innerHTML = "<div>" + userInput + "</div>";
}
''',
        "Array Mutation & Async Error Handling": '''async function fetchUserData(userId) {
    // Quality & Bug: Missing try/catch around async call and using == comparison
    const response = await fetch("https://api.example.com/users/" + userId);
    const data = await response.json();
    if (data.status == 200) {
        return data.user;
    }
}
''',
    }
}
