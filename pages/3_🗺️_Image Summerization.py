import requests
from PIL import Image
import getpass
import os
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
    

st.set_page_config(
    page_title="Image Summerization",
    page_icon="🗺️",
)



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
        
    st.title("Image Summerization")

    image_question = st.text_input("Type your question here:")

    # upload local image
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_url = uploaded_file.name
    else:
        # image = "https://picsum.photos/seed/picsum/300/300"
        image = Image.open("./static/sample_image.jpeg")

    st.image(image, caption='Uploaded Image', width=300)

    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": image_question,
            },  
            {"type": "image_url", "image_url": image},
        ]
    )


    response = llm.invoke([message]).content

    if image_question:
        st.text_area("Chatbot Response:", response, height=30)
    else:
        st.text_area("Chatbot Response:", "Please type your question above", height=50)















    authenticator.logout()
    
    
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')