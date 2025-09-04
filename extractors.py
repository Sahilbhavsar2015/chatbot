import re
from llm_service import extract_with_llm

def extract_name(text):
    match = re.search(r'([A-Z][a-z]+\s[A-Z][a-z]+)', text.strip())
    return match.group(1).strip() if match else extract_with_llm("person's full name", text)

def extract_age(text):
    match = re.search(r'\b([1-9][0-9]?|1[01][0-9]|120)\b', text)
    return int(match.group(1)) if match else extract_with_llm("age in years (number)", text)

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
    return digits if 10 <= len(digits) <= 14 else extract_with_llm("mobile/phone number", text)

def extract_country(text):
    return extract_with_llm("country name", text)

def extract_profession(text):
    return extract_with_llm("profession or job title", text)

EXTRACTORS = {
    "full_name": extract_name,
    "age": extract_age,
    "gender": extract_gender,
    "email": extract_email,
    "mobile": extract_mobile,
    "country": extract_country,
    "profession": extract_profession
}
