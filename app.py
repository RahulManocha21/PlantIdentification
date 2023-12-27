from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image], stream=True)
    return response

##initialize our streamlit app

st.set_page_config(page_title="🪴 Plant Identification")

st.header("Plant Identification")
#input=st.text_input("Ask Question",key="input")
uploaded_file = st.file_uploader("Choose an 🪴 image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Get Response")

## If ask button is clicked

if submit:
    input = """You are a botanical expert, study the image and response accordingly,
    You have to identify the plant and check for the disease if any, if any disease found give the cure steps
    if there is no disease found, then give the steps to how to care for that plant to keep healthy.
    You also need to highlight the point that the diseases are found or not make that bold in the response.
    """
    response=get_gemini_response(input,image)
    st.subheader("Response : ")
    for chunks in response:
        st.write(chunks.text)