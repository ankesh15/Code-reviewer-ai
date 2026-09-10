"""
AI Code Reviewer — Streamlit Application
A clean, minimal, automated AI code reviewer that automatically detects language
and performs a comprehensive 360-degree review across Bugs, Security, Performance,
Code Quality, Complexity, Recommendations, and Refactored Code.
"""

from dotenv import load_dotenv
load_dotenv(override=True)

import streamlit as st
from reviewer import CodeReviewer, get_api_key

# 1. Page Configuration (No sidebar, clean centered layout)
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Main Page Header
st.title("AI Code Reviewer")
st.markdown(
    "Paste your code and get an AI-powered review for bugs, security, performance, code quality, and complexity."
)

# 3. Code Editor
code_input = st.text_area(
    label="Source Code",
    height=320,
    placeholder="Paste your Python, JavaScript, TypeScript, C++, Java, C, or Go code here...",
    label_visibility="collapsed",
)

review_clicked = st.button("🔍 Review Code", type="primary", use_container_width=True)


def render_issue_list(issues_list, empty_msg: str):
    """Renders issues for a specific review pillar with severity indicators."""
    if not issues_list:
        st.caption(f"✓ {empty_msg}")
        return

    severity_icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
    for issue in issues_list:
        sev = issue.get("severity", "MEDIUM")
        icon = severity_icons.get(sev, "⚪")
        line_ref = f" (Line {issue['line']})" if issue.get("line") else ""
        problem_title = issue.get("problem", "Unspecified Issue")

        with st.expander(f"{icon} **[{sev}]** {problem_title}{line_ref}", expanded=(sev == "HIGH")):
            if issue.get("explanation"):
                st.markdown(f"**Explanation:**\n{issue['explanation']}")
            if issue.get("suggested_fix"):
                st.markdown(f"**Suggested Fix:**\n`{issue['suggested_fix']}`")


# 4. Review Execution
if review_clicked:
    if not code_input.strip():
        st.warning("Please paste some code to review.")
    else:
        # Check API key configuration securely (never display the key)
        api_key = get_api_key()
        if not api_key:
            st.error("Gemini API key is not configured. Please configure GEMINI_API_KEY in your environment.")
        else:
            with st.spinner("Analyzing code for bugs, security, performance, and quality..."):
                reviewer = CodeReviewer()
                review_data = reviewer.review(code=code_input)

            # Check for configuration or communication error
            if "_error" in review_data and review_data.get("overall_score", 0) == 0:
                st.error(review_data.get("summary", "An error occurred during analysis."))
                if review_data.get("_error") != review_data.get("summary"):
                    st.caption(f"Details: {review_data.get('_error')}")
            else:
                st.markdown("---")
                st.header("AI Analysis")

                detected_lang = review_data.get("detected_language", "Auto-Detected")
                score = review_data.get("overall_score", 5)

                col_lang, col_score = st.columns(2)
                with col_lang:
                    st.markdown(f"**Detected Language:** `{detected_lang}`")
                with col_score:
                    st.markdown(f"**Overall Score:** `{score} / 10`")

                # Summary
                st.subheader("Summary")
                st.info(review_data.get("summary", "No summary available."))

                # Categorize issues
                all_issues = review_data.get("issues", [])
                bugs = [i for i in all_issues if i.get("category") == "BUG"]
                security = [i for i in all_issues if i.get("category") == "SECURITY"]
                performance = [i for i in all_issues if i.get("category") == "PERFORMANCE"]
                quality = [i for i in all_issues if i.get("category") == "QUALITY"]

                # 🐛 Bugs
                st.subheader("🐛 Bugs")
                render_issue_list(bugs, "No critical bugs or edge-case errors detected.")

                # 🔐 Security
                st.subheader("🔐 Security")
                render_issue_list(security, "No critical security vulnerabilities or unsafe operations detected.")

                # ⚡ Performance
                st.subheader("⚡ Performance")
                render_issue_list(performance, "No algorithmic bottlenecks or significant performance issues detected.")

                # ✨ Code Quality
                st.subheader("✨ Code Quality")
                render_issue_list(quality, "Code conforms to standard quality and readability conventions.")

                # 📊 Complexity
                st.subheader("📊 Complexity")
                complexity = review_data.get("complexity", {})
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    st.markdown(f"**Time Complexity:** `{complexity.get('time', 'N/A')}`")
                with c_col2:
                    st.markdown(f"**Space Complexity:** `{complexity.get('space', 'N/A')}`")

                # 💡 Recommendations
                st.subheader("💡 Recommendations")
                suggestions = review_data.get("suggestions", [])
                if suggestions:
                    for s in suggestions:
                        st.markdown(f"- {s}")
                else:
                    st.caption("No specific recommendations provided.")

                # 🔧 Improved Code
                st.subheader("🔧 Improved Code")
                fixed_code = review_data.get("fixed_code", "").strip()
                if fixed_code:
                    # Map detected language to syntax highlighter string
                    lang_lower = detected_lang.lower()
                    code_lang = "python"
                    if "c++" in lang_lower or "cpp" in lang_lower:
                        code_lang = "cpp"
                    elif "javascript" in lang_lower or "js" in lang_lower:
                        code_lang = "javascript"
                    elif "typescript" in lang_lower or "ts" in lang_lower:
                        code_lang = "typescript"
                    elif "java" in lang_lower:
                        code_lang = "java"
                    elif "go" in lang_lower:
                        code_lang = "go"
                    elif "c" == lang_lower or "c " in lang_lower:
                        code_lang = "c"

                    st.code(fixed_code, language=code_lang)
                else:
                    st.caption("No modified code replacement needed.")