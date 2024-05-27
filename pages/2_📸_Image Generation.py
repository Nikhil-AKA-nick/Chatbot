from langchain_community.llms import Replicate
import os
import getpass
from PIL import Image
import urllib.request
from dotenv import load_dotenv
import streamlit as st
import streamlit_authenticator as stauth

load_dotenv()

if "REPLICATE_API_TOKEN" not in os.environ:
    os.environ["REPLICATE_API_TOKEN"] = getpass.getpass("Provide your Google API Key")

st.set_page_config(
    page_title="Image Generator",
    page_icon="📸",
)


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

    text2image = Replicate(
        model="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        model_kwargs={"image_dimensions": "512x512"},
    )

    st.title('Image Generator')

    user_input = st.text_input("Enter a description of the image you want to generate:")

    if user_input:
        image_url = text2image(user_input)

        urllib.request.urlretrieve(image_url, "static/image_cache/downloaded_image.jpg")

        image = Image.open("static/image_cache/downloaded_image.jpg")

        st.image(image, caption='Generated Image')

        # os.remove("downloaded_image.jpg")
        
    authenticator.logout()
    
    
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')