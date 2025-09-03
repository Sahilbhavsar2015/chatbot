import streamlit as st
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="Personal Details Assistant", 
    layout="centered"
)

@st.cache_resource
def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set OPENAI_API_KEY in your .env file")
        st.stop()
    return ChatOpenAI(temperature=0, model="gpt-4o-mini", openai_api_key=api_key)

llm = get_llm()

FIELDS_CONFIG = [
    {"name": "Full Name", "key": "full_name", "question": "Hi! What's your full name?", "validation_msg": "Please enter a valid name (letters only)"},
    {"name": "Age", "key": "age", "question": "How old are you?", "validation_msg": "Please enter age between 1-120"},
    {"name": "Gender", "key": "gender", "question": "What's your gender? (Male/Female/Other)", "validation_msg": "Please choose: Male, Female, or Other"},
    {"name": "Email", "key": "email", "question": "What's your email address?", "validation_msg": "Please enter a valid email address"},
    {"name": "Mobile", "key": "mobile", "question": "What's your mobile number?", "validation_msg": "Please enter 10-14 digit mobile number"},
    {"name": "Country", "key": "country", "question": "Which country are you from?", "validation_msg": "Please enter a valid country name"},
    {"name": "Profession", "key": "profession", "question": "What's your profession?", "validation_msg": "Please enter your profession"}
]

def extract_with_llm(field_name, text):
    prompt = PromptTemplate.from_template(
        "Extract only the {field} from: '{text}'. Return just the value, no extra words. If not found, return 'NONE'."
    )
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"field": field_name, "text": text})
    return result.strip() if result and result.upper() != "NONE" else None

def extract_name(text):
    match = re.search(r'([A-Z][a-z]+\s[A-Z][a-z]+)', text.strip())
    if match:
        return match.group(1).strip()
    return extract_with_llm("person's full name", text)

def extract_age(text):
    match = re.search(r'\b([1-9][0-9]?|1[01][0-9]|120)\b', text)
    if match:
        return int(match.group(1))
    return extract_with_llm("age in years (number)", text)

def extract_gender(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["male", "man", "boy"]) and "female" not in text_lower:
        return "Male"
    elif any(word in text_lower for word in ["female", "woman", "girl"]):
        return "Female"
    elif any(word in text_lower for word in ["other", "non-binary", "transgender"]):
        return "Other"
    return extract_with_llm("gender (Male/Female/Other)", text)

def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else extract_with_llm("email address", text)

def extract_mobile(text):
    digits = re.sub(r'[^\d]', '', text)
    if 10 <= len(digits) <= 14:
        return digits
    return extract_with_llm("mobile/phone number", text)

def extract_country(text):
    return extract_with_llm("country name", text)

def extract_profession(text):
    return extract_with_llm("profession or job title", text)

def validate_name(name):
    return name and re.match(r'^[A-Za-z\s]+$', name.strip()) and len(name.strip()) >= 2

def validate_age(age):
    return isinstance(age, int) and 1 <= age <= 120

def validate_gender(gender):
    return gender in ["Male", "Female", "Other"]

def validate_email(email):
    return email and re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email)

def validate_mobile(mobile):
    return mobile and mobile.isdigit() and 10 <= len(mobile) <= 14

def validate_country(country):
    return country and re.match(r'^[A-Za-z\s]+$', country.strip()) and len(country.strip()) >= 2

def validate_profession(profession):
    return profession and re.match(r'^[A-Za-z\s]+$', profession.strip()) and len(profession.strip()) >= 2

EXTRACTORS = {
    "full_name": extract_name,
    "age": extract_age,
    "gender": extract_gender,
    "email": extract_email,
    "mobile": extract_mobile,
    "country": extract_country,
    "profession": extract_profession
}

VALIDATORS = {
    "full_name": validate_name,
    "age": validate_age,
    "gender": validate_gender,
    "email": validate_email,
    "mobile": validate_mobile,
    "country": validate_country,
    "profession": validate_profession
}

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_step = 0
        st.session_state.collected_data = {}
        st.session_state.waiting_for_input = True
        st.session_state.validation_error = False
        welcome_msg = "Hello! I'm your personal details assistant. Let's get started!"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        first_question = FIELDS_CONFIG[0]['question']
        st.session_state.messages.append({"role": "assistant", "content": f"{first_question}"})

def process_user_input(user_input):
    current_field = FIELDS_CONFIG[st.session_state.current_step]
    field_key = current_field["key"]
    extractor = EXTRACTORS[field_key]
    extracted_value = extractor(user_input)
    if extracted_value is not None:
        validator = VALIDATORS[field_key]
        is_valid = validator(extracted_value)
        if is_valid:
            st.session_state.collected_data[field_key] = extracted_value
            st.session_state.validation_error = False
            confirm_msg = f"Great! I've recorded your {current_field['name']}: **{extracted_value}**"
            st.session_state.messages.append({"role": "assistant", "content": confirm_msg})
            st.session_state.current_step += 1
            if st.session_state.current_step < len(FIELDS_CONFIG):
                next_field = FIELDS_CONFIG[st.session_state.current_step]
                st.session_state.messages.append({"role": "assistant", "content": f"{next_field['question']}"})
            else:
                show_summary()
        else:
            st.session_state.validation_error = True
            error_msg = f"{current_field['validation_msg']}. Please try again."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        st.session_state.validation_error = True
        error_msg = f"I couldn't extract your {current_field['name'].lower()} from that. {current_field['validation_msg']}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

def show_summary():
    st.session_state.waiting_for_input = False
    summary = "**Perfect! Here's your complete profile:**\n\n"
    for field in FIELDS_CONFIG:
        key = field["key"]
        value = st.session_state.collected_data.get(key, "Not provided")
        summary += f"**{field['name']}**: {value}  \n"
    summary += "\n**Thank you for providing all your details!**"
    st.session_state.messages.append({"role": "assistant", "content": summary})

def main():
    st.title("Personal Details Assistant")
    init_session_state()
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    if st.session_state.waiting_for_input and st.session_state.current_step < len(FIELDS_CONFIG):
        if user_input := st.chat_input("Type your response here..."):
            with chat_container:
                with st.chat_message("user"):
                    st.write(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            process_user_input(user_input)
            st.rerun()

if __name__ == "__main__":
    main()
