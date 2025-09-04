import re

def validate_name(name): return bool(name and re.match(r'^[A-Za-z\s]+$', name.strip()))
def validate_age(age): return isinstance(age, int) and 1 <= age <= 120
def validate_gender(gender): return gender in ["Male", "Female", "Other"]
def validate_email(email): return bool(email and re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email))
def validate_mobile(mobile): return bool(mobile and mobile.isdigit() and 10 <= len(mobile) <= 14)
def validate_country(country): return bool(country and re.match(r'^[A-Za-z\s]+$', country.strip()))
def validate_profession(profession): return bool(profession and re.match(r'^[A-Za-z\s]+$', profession.strip()))

VALIDATORS = {
    "full_name": validate_name,
    "age": validate_age,
    "gender": validate_gender,
    "email": validate_email,
    "mobile": validate_mobile,
    "country": validate_country,
    "profession": validate_profession
}
