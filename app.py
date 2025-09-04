import streamlit as st
from state_manager import init_session_state, process_user_input
from config import FIELDS_CONFIG

st.set_page_config(page_title="Personal Details Assistant", layout="centered")

def main():
    st.title("Personal Details Assistant")

    # Initialize state
    init_session_state()

    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # User input
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
