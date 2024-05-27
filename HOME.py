import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

allow_dangerous_deserialization = True
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
    
    st.write("# Welcome to ChatAI 👋")

    st.sidebar.success("Select a feature above.")

    st.markdown(
        """
        Greetings, future AI enthusiast!

        ChatAI is a chatbot that can answer your questions about almost anything.

        It has amazing capabilities and is currently in development.

        Some of it's capabilities include: Question Answering, Image Generation, Image Summerization, PDF summerization.

        
        Developed with ❤️ by Prathamesh Zade, Nikhil Sonone, Abhishek Gambhire and Chaitanya Sonawane.
        """
    )

    authenticator.logout()
    
    
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

