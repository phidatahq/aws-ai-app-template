import os
from typing import Optional, List, Dict

import openai
import streamlit as st
from streamlit_chat import message


#
# -*- Create Sidebar
#
def chatbot_sidebar():
    st.sidebar.markdown("## Chatbot Settings")

    # Get OpenAI API key from environment variable
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    # If not found, get it from user input
    if OPENAI_API_KEY is None:
        api_key = st.sidebar.text_input("OpenAI API key", value="sk-***", key="api_key")
        if api_key != "sk-***":
            OPENAI_API_KEY = api_key
    # Store it in session state and environment variable
    if OPENAI_API_KEY is not None:
        st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    st.sidebar.markdown("---")
    st.sidebar.markdown("## Chatbot Status")
    if "OPENAI_API_KEY" in st.session_state:
        st.sidebar.markdown("🔑  OpenAI API key set")


def generate_response(messages: List[Dict[str, str]]) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1,
        # stream=True,
        max_tokens=2048,
    )
    # st.write(completion)
    response = completion.choices[0].message
    return response


#
# -*- Create Main Page
#
def chatbot_main():
    # Create session variable to store the chat
    if "all_messages" not in st.session_state:
        st.session_state["all_messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    user_message = st.text_input("Message:", key="input")
    if user_message:
        new_message = {"role": "user", "content": user_message}
        st.session_state["all_messages"].append(new_message)

        # Generate response
        output = generate_response(st.session_state["all_messages"])
        # Store the output
        st.session_state["all_messages"].append(output)

    if st.session_state["all_messages"]:
        for msg in st.session_state["all_messages"]:
            if msg["role"] == "user":
                message(msg["content"], is_user=True)
            elif msg["role"] == "assistant":
                message(msg["content"])


#
# -*- Run the app
#
st.markdown("# Chatting with GPT-3.5 Turbo")
st.write("This is a chatbot built using OpenAI. Send it a message and it will respond.")

chatbot_sidebar()
chatbot_main()
