import getpass
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

llm = ChatGoogleGenerativeAI(model="gemini-pro")

st.set_page_config(
    page_title="Question Answering",
    page_icon="❔",
)

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"]:

    st.title("Chatbot")

    # Initialize session state for conversation history
    if "history" not in st.session_state:
        st.session_state["history"] = []

    user_input = st.text_input("Type your question here:")

    def truncate_response(response, max_words=100):
        words = response.split()
        if len(words) > max_words:
            words = words[:max_words]
            return ' '.join(words) + '...'
        return response

    if user_input:
        result = llm.invoke(user_input)
        
        # Truncate the response to 100 words
        truncated_response = truncate_response(result.content)
        
        # Append the user input and truncated response to the history
        st.session_state["history"].append({"user": user_input, "bot": truncated_response})

    # Display conversation history
    for chat in st.session_state["history"]:
        st.write(f"You: {chat['user']}")
        st.write(f"Bot: {chat['bot']}")

    authenticator.logout()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
