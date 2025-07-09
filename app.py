import streamlit as st
import google.generativeai as genai
import os
import re

genai.configure(api_key=os.getenv("GENAI_API_KEY", ""))

if not os.getenv("GENAI_API_KEY"):
    st.warning("Google Generative AI API key not set. Please set the GENAI_API_KEY environment variable.")

sys_prompt = """ You are a helpful AI Python Code Reviewer. 
When students provide Python code, you will:
1. Provide a detailed **Code Review** of the code.
2. Highlight any issues or errors in a section labeled **Bug Report**.
3. Provide a corrected version of the code in a section labeled **Fixed Code**.

Always format your response exactly like this:
- Code Review:(make it bold as title)
  [Your review here]

- Bug Report:(make it bold as title)
  [List of bugs here]

- Fixed Code:(make it bold as title)
  [Corrected Python code here]

If there are no bugs, clearly state that in the Bug Report section and still provide a reviewed version of the code in Fixed Code.

Do not respond to anything unrelated to Python code. """

llm = genai.GenerativeModel("models/gemini-1.5-flash",
                            system_instruction= sys_prompt)

st.title('GenAI App - AI Code Reviewer')

human_prompt = st.text_area("Enter your Python code here ...")

if st.button("Generate"):
    if human_prompt:
        try:
            response = llm.generate_content(human_prompt)
            response_text = response.text

            # Parse the response into sections
            def extract_section(text, section):
                pattern = rf"- {section}:(.*?)((?=\n- [A-Za-z ]+:)|\Z)"
                match = re.search(pattern, text, re.DOTALL)
                return match.group(1).strip() if match else None

            code_review = extract_section(response_text, "Code Review")
            bug_report = extract_section(response_text, "Bug Report")
            fixed_code = extract_section(response_text, "Fixed Code")

            st.subheader("Code Review")
            if code_review:
                st.write(code_review)
            else:
                st.warning("Code Review section not found in response.")

            st.subheader("Bug Report")
            if bug_report:
                st.write(bug_report)
            else:
                st.warning("Bug Report section not found in response.")

            st.subheader("Fixed Code")
            if fixed_code:
                st.code(fixed_code, language="python")
            else:
                st.warning("Fixed Code section not found in response.")
        except Exception as e:
            st.error(f"Error generating review: {e}")
    else:
        st.warning("Please enter Python code before clicking Generate.")