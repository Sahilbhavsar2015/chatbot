# Personal Details Workflow Bot (LangChain + Streamlit)

This project is an interactive workflow chatbot built with LangChain and Streamlit. The bot will sequentially collect, extract, and validate 7 personal details:

- Full Name
- Age
- Gender
- Email Address
- Mobile Number
- Country
- Profession

## Features

- Guided step-by-step data collection (one question at a time)
- Entity extraction (gets only the required value from user input)
- Built-in validation (regex and/or LLM-based parsing)
- Live summary of collected data once complete
- Modern frontend with Streamlit

## Setup

1. **Clone the repository**
2. **Install dependencies**
  - create venv using command - python venv venv
  - pip install -r requirements.txt

3. **OpenApi Key**
 - Ensure your OpenAI API key is properly set in the .env file before running the application. The app will display an error message if the API key is missing.

## Running the App
- Run the application using below command
- streamlit run main.py

