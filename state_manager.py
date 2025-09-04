import streamlit as st
from config import FIELDS_CONFIG
from extractors import EXTRACTORS
from validators import VALIDATORS

def init_session_state():
    """Initialize chat state if not already set."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_step = 0
        st.session_state.collected_data = {}
        st.session_state.waiting_for_input = True
        st.session_state.validation_error = False

        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Hello! I'm your personal details assistant. Let's get started!"
        })
        st.session_state.messages.append({
            "role": "assistant", 
            "content": FIELDS_CONFIG[0]['question']
        })

def process_user_input(user_input):
    """Process user response for the current field."""
    current_field = FIELDS_CONFIG[st.session_state.current_step]
    field_key = current_field["key"]

    extractor = EXTRACTORS[field_key]
    extracted_value = extractor(user_input)

    if extracted_value:
        validator = VALIDATORS[field_key]
        if validator(extracted_value):
            # Save valid response
            st.session_state.collected_data[field_key] = extracted_value
            st.session_state.validation_error = False

            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Great! I've recorded your {current_field['name']}: **{extracted_value}**"
            })

            # Move to next question
            st.session_state.current_step += 1
            if st.session_state.current_step < len(FIELDS_CONFIG):
                next_field = FIELDS_CONFIG[st.session_state.current_step]
                st.session_state.messages.append({"role": "assistant", "content": next_field['question']})
            else:
                show_summary()
        else:
            st.session_state.validation_error = True
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"{current_field['validation_msg']}. Please try again."
            })
    else:
        st.session_state.validation_error = True
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"I couldn't extract your {current_field['name'].lower()} from that. {current_field['validation_msg']}"
        })

def show_summary():
    """Display collected profile summary."""
    st.session_state.waiting_for_input = False
    summary = "**Perfect! Here's your complete profile:**\n\n"
    for field in FIELDS_CONFIG:
        key = field["key"]
        value = st.session_state.collected_data.get(key, "Not provided")
        summary += f"**{field['name']}**: {value}  \n"
    summary += "\n**Thank you for providing all your details!**"
    st.session_state.messages.append({"role": "assistant", "content": summary})
