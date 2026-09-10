#!/usr/bin/env python3
"""
Evaluation Runner for AI Code Reviewer.
Runs curated test cases through the review pipeline and computes detection accuracy,
false negatives, and category-level precision metrics.
Supports a `--mock` mode for deterministic evaluation without API quotas.
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

# Ensure parent directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from reviewer import CodeReviewer
from utils.helpers import clean_and_parse_json

TEST_CASES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_cases.json")


def load_test_cases(limit: int = 0) -> List[Dict[str, Any]]:
    """Loads curated evaluation test cases from JSON file."""
    if not os.path.exists(TEST_CASES_PATH):
        raise FileNotFoundError(f"Test cases file not found at: {TEST_CASES_PATH}")

    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    if limit > 0:
        return cases[:limit]
    return cases


def generate_mock_review(test_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a deterministic review response for mock evaluation mode.
    Accurately mirrors real LLM response structure for offline benchmarking.
    """
    category = test_case.get("expected_category", "QUALITY")
    name = test_case.get("name", "Defect")

    return {
        "overall_score": 4,
        "summary": f"Detected significant issues in {name}.",
        "issues": [
            {
                "severity": "HIGH",
                "category": category,
                "line": 2,
                "problem": f"Identified {name}",
                "explanation": test_case.get("description", "Identified code defect."),
                "suggested_fix": "Refactor snippet following engineering guidelines."
            }
        ],
        "suggestions": ["Follow language guidelines to prevent this defect."],
        "complexity": {"time": "O(n)", "space": "O(1)"},
        "fixed_code": "# Refactored code would be generated here."
    }


def run_evaluation(
    mode: str = "Full Review",
    mock: bool = False,
    limit: int = 0,
    api_key: str = "",
    delay_sec: float = 1.0,
) -> Dict[str, Any]:
    """
    Executes review against each test case and computes evaluation metrics.
    """
    cases = load_test_cases(limit=limit)
    print(f"\n========================================================")
    print(f"   AI Code Reviewer - Automated Evaluation Suite")
    print(f"========================================================")
    print(f"Test Cases Loaded : {len(cases)}")
    print(f"Review Mode       : {mode}")
    print(f"Execution Mode    : {'Simulated (Mock)' if mock else 'Live Gemini API'}")
    print(f"--------------------------------------------------------\n")

    reviewer = None if mock else CodeReviewer(api_key=api_key)
    if not mock and not reviewer.is_configured():
        print("ERROR: No valid Gemini API key found.")
        print("Please set GEMINI_API_KEY environment variable or pass --api-key.")
        print("Tip: Run with `--mock` to verify the evaluation pipeline without an API key.")
        sys.exit(1)

    results = []
    category_stats: Dict[str, Dict[str, int]] = {
        "SECURITY": {"expected": 0, "detected": 0},
        "BUG": {"expected": 0, "detected": 0},
        "PERFORMANCE": {"expected": 0, "detected": 0},
        "QUALITY": {"expected": 0, "detected": 0},
    }

    total_issues_flagged = 0
    start_time = time.time()

    for idx, tc in enumerate(cases, 1):
        tc_id = tc["id"]
        tc_name = tc["name"]
        lang = tc["language"]
        code = tc["code"]
        expected_cat = tc["expected_category"].upper()

        if expected_cat in category_stats:
            category_stats[expected_cat]["expected"] += 1

        print(f"[{idx:02d}/{len(cases):02d}] Evaluating {tc_id}: {tc_name} ({lang})... ", end="", flush=True)

        if mock:
            review_res = generate_mock_review(tc)
        else:
            review_res = reviewer.review(code=code, language=lang, mode=mode)
            if delay_sec > 0:
                time.sleep(delay_sec)

        issues = review_res.get("issues", [])
        total_issues_flagged += len(issues)

        # Extract detected categories
        detected_categories = {
            item.get("category", "").upper() for item in issues if isinstance(item, dict)
        }

        hit = expected_cat in detected_categories
        if hit:
            if expected_cat in category_stats:
                category_stats[expected_cat]["detected"] += 1
            print("✓ DETECTED")
        else:
            print(f"✗ MISSED (Expected {expected_cat}, got {detected_categories or 'None'})")

        results.append({
            "id": tc_id,
            "name": tc_name,
            "expected": expected_cat,
            "detected_categories": list(detected_categories),
            "hit": hit,
            "issue_count": len(issues),
            "score": review_res.get("overall_score"),
        })

    elapsed = time.time() - start_time
    total_cases = len(cases)
    total_hits = sum(1 for r in results if r["hit"])
    overall_detection_rate = (total_hits / total_cases * 100) if total_cases > 0 else 0.0

    # Print Summary Report
    print(f"\n========================================================")
    print(f"                 EVALUATION SUMMARY")
    print(f"========================================================")
    print(f"Total Test Cases   : {total_cases}")
    print(f"Expected Detected  : {total_hits} / {total_cases}")
    print(f"Overall Detection  : {overall_detection_rate:.1f}%")
    print(f"Total Issues Found : {total_issues_flagged}")
    print(f"Time Elapsed       : {elapsed:.2f}s")
    print(f"--------------------------------------------------------")
    print(f"{'Category':<15} | {'Expected':<10} | {'Detected':<10} | {'Accuracy':<10}")
    print(f"--------------------------------------------------------")

    for cat, stats in category_stats.items():
        exp = stats["expected"]
        det = stats["detected"]
        rate = (det / exp * 100) if exp > 0 else 0.0
        print(f"{cat:<15} | {exp:<10} | {det:<10} | {rate:.1f}%")

    print(f"--------------------------------------------------------")

    # Missed test cases (False Negatives)
    missed = [r for r in results if not r["hit"]]
    if missed:
        print("\nFalse Negatives (Missed Expected Issues):")
        for m in missed:
            print(f" - [{m['id']}] {m['name']} (Expected: {m['expected']}, Detected: {m['detected_categories']})")
    else:
        print("\nAll expected categories successfully flagged!")

    print(f"========================================================\n")

    return {
        "total_cases": total_cases,
        "total_hits": total_hits,
        "detection_rate": overall_detection_rate,
        "total_issues": total_issues_flagged,
        "category_stats": category_stats,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Evaluate AI Code Reviewer against curated test cases.")
    parser.add_argument("--mock", action="store_true", help="Run evaluation in mock simulation mode.")
    parser.add_argument("--mode", default="Full Review", help="Review mode (e.g. 'Full Review', 'Bug Detection').")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of test cases to evaluate.")
    parser.add_argument("--api-key", default="", help="Explicit Gemini API key.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds between API calls to respect rate limits.")

    args = parser.parse_args()
    run_evaluation(
        mode=args.mode,
        mock=args.mock,
        limit=args.limit,
        api_key=args.api_key,
        delay_sec=args.delay,
    )


if __name__ == "__main__":
    main()
