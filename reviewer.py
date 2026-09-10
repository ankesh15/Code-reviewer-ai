"""
Core reviewer engine for AI Code Reviewer.
Coordinates Gemini API communication, context injection, prompt engineering,
and resilient structured JSON parsing with comprehensive error handling.
Supports automatic language detection and comprehensive multi-pillar review.
"""

import os
import warnings
from typing import Any, Dict, Optional

# Suppress deprecation warnings from upstream google.generativeai
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai

from prompts import SYSTEM_PERSONA, build_prompt, build_comprehensive_prompt
from utils.helpers import load_guidelines, clean_and_parse_json

# Load environment variables from .env if present
load_dotenv(override=True)

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
MAX_CODE_CHARS = 50000


def get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """
    Resolves the Google Generative AI API key from:
    1. Explicit key argument (e.g. for CLI testing)
    2. Streamlit secrets (for cloud deployments)
    3. GEMINI_API_KEY environment variable
    4. GENAI_API_KEY environment variable (backward compatibility)

    Never displays or logs the actual secret key.
    """
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    # Check Streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "GEMINI_API_KEY" in st.secrets:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
            if "GENAI_API_KEY" in st.secrets:
                return str(st.secrets["GENAI_API_KEY"]).strip()
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY") or None


class CodeReviewer:
    """
    Manages LLM initialization and automated code review execution.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = get_api_key(api_key)
        self.model_name = model_name or DEFAULT_MODEL
        self._configured = False

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self._configured = True

    def is_configured(self) -> bool:
        """Returns True if a valid API key is configured."""
        return bool(self.api_key and self._configured)

    def review(
        self,
        code: str,
        language: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Performs structured code analysis on the provided code snippet.
        If language is None or 'auto', automatically detects programming language
        and conducts a comprehensive 360-degree review covering Bugs, Security,
        Performance, Code Quality, and Algorithmic Complexity.
        """
        # 1. Validate inputs
        if not code or not code.strip():
            return {
                "detected_language": "Unknown",
                "overall_score": 0,
                "summary": "No code provided for review.",
                "issues": [],
                "suggestions": ["Please enter or paste a valid code snippet to review."],
                "complexity": {"time": "N/A", "space": "N/A"},
                "fixed_code": "",
                "_error": "Empty input code.",
            }

        if len(code) > MAX_CODE_CHARS:
            return {
                "detected_language": "Unknown",
                "overall_score": 0,
                "summary": f"Code length exceeds the maximum supported threshold ({len(code)} / {MAX_CODE_CHARS} characters).",
                "issues": [
                    {
                        "severity": "HIGH",
                        "category": "QUALITY",
                        "line": None,
                        "problem": "Input snippet too large",
                        "explanation": f"Input size ({len(code)} chars) exceeds safe processing limits.",
                        "suggested_fix": "Submit smaller, modular functions or snippets for review."
                    }
                ],
                "suggestions": ["Break down large scripts into individual functions for focused analysis."],
                "complexity": {"time": "N/A", "space": "N/A"},
                "fixed_code": "",
                "_error": "Input length exceeded.",
            }

        if not self.is_configured():
            return {
                "detected_language": "Unknown",
                "overall_score": 0,
                "summary": "Gemini API key is not configured. Please configure GEMINI_API_KEY in your environment.",
                "issues": [],
                "suggestions": [
                    "Add GEMINI_API_KEY=your_key_here to a local .env file",
                    "Or export GEMINI_API_KEY in your terminal environment."
                ],
                "complexity": {"time": "N/A", "space": "N/A"},
                "fixed_code": "",
                "_error": "Gemini API key is not configured. Please configure GEMINI_API_KEY in your environment.",
            }

        # 2. Context & Prompt Construction
        # Automatic language detection & comprehensive mode if not specified
        if not language or language.lower() == "auto" or not mode:
            guidelines = load_guidelines()
            prompt = build_comprehensive_prompt(code=code, guidelines=guidelines)
        else:
            guidelines = load_guidelines(language)
            prompt = build_prompt(
                code=code,
                language=language,
                mode=mode,
                guidelines=guidelines,
            )

        # 3. Invoke Gemini with structured JSON configuration (with retry on transient rate limits)
        max_retries = 2
        last_exception = None

        for attempt in range(max_retries + 1):
            try:
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=SYSTEM_PERSONA,
                    generation_config={
                        "response_mime_type": "application/json",
                        "temperature": 0.2,
                    },
                )
                response = model.generate_content(prompt)

                if not response or not response.text:
                    raise ValueError("Model returned an empty response.")

                # 4. Robust JSON parsing and normalization
                parsed_result = clean_and_parse_json(response.text)
                parsed_result["_raw_response"] = response.text
                return parsed_result

            except Exception as exc:
                last_exception = exc
                err_str = str(exc).lower()
                if ("429" in err_str or "quota" in err_str or "resource_exhausted" in err_str) and attempt < max_retries:
                    import time
                    time.sleep(6 * (attempt + 1))
                    continue
                break

        try:
            raise last_exception

        except Exception as exc:
            err_msg = str(exc)
            user_friendly_explanation = (
                "An error occurred while communicating with the Gemini API. "
                "Check your network connection or API quota."
            )
            if "API_KEY_INVALID" in err_msg or "invalid api key" in err_msg.lower():
                user_friendly_explanation = "The configured Gemini API key is invalid or has expired."
            elif "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                user_friendly_explanation = "Gemini API quota or rate limit exceeded. Please wait a moment."

            return {
                "detected_language": "Auto-Detected",
                "overall_score": 0,
                "summary": f"API Error: {user_friendly_explanation}",
                "issues": [
                    {
                        "severity": "HIGH",
                        "category": "QUALITY",
                        "line": None,
                        "problem": "API Communication Failure",
                        "explanation": f"Detailed error: {err_msg}",
                        "suggested_fix": "Verify that GEMINI_API_KEY is configured properly and quota is available."
                    }
                ],
                "suggestions": [
                    "Ensure your network connection can reach Google API endpoints.",
                    "Verify your Gemini API key has quota available at Google AI Studio."
                ],
                "complexity": {"time": "N/A", "space": "N/A"},
                "fixed_code": "",
                "_error": err_msg,
            }
