# GenAI App - AI Code Reviewer

This project is an AI-powered Python code reviewer built using Streamlit and Google's Generative AI.

## Features
- Code review
- Bug detection
- Code correction suggestions

![Screenshot 2024-11-30 003454](https://github.com/user-attachments/assets/3317706e-a466-4b4e-8ad3-9cb5188bbe94)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/mejdihaddad/GenAI-App-AI-Code-Reviewer.git
   cd GenAI-App-AI-Code-Reviewer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Google Generative AI API key**
   - Obtain your API key from Google.
   - Set it as an environment variable:
     - On Linux/macOS:
       ```bash
       export GENAI_API_KEY=your_api_key_here
       ```
     - On Windows (Command Prompt):
       ```cmd
       set GENAI_API_KEY=your_api_key_here
       ```
     - On Windows (PowerShell):
       ```powershell
       $env:GENAI_API_KEY="your_api_key_here"
       ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Dependencies

This app only requires the following Python packages:
- streamlit
- google-generativeai

All other dependencies have been removed to keep the environment lean and setup simple.
