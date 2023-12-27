import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the API key directly (not from .env)
genai.configure(api_key=st.secrets["SecretKey"]["GOOGLE_API_KEY"])

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image])
    return response.text

# initialize our streamlit app
st.set_page_config(page_title="🪴 Plant Identification")
st.header("Plant Identification")

# Input for the user to ask a question
input_question = st.text_input("Ask a question about the plant")

option = st.radio("Select image source:", ("Upload Image", "Capture from Camera"))

if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an 🪴 image...", type=["jpg", "jpeg", "png"])
elif option =='Capture from Camera':
    uploaded_file = st.camera_input('Camera Access', label_visibility="visible")
    
# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to trigger the response
submit = st.button("Get Response")

# If the button is clicked
if submit:
    if input_question and image:
        input_text = f"You are a botanical expert, study the image and respond accordingly. If there is no plant in the image, respond as No plant found. else {input_question}, Write your answer in layman's terms with less technicalities, so everyone can understand."
        response = get_gemini_response(input_text, image)

        # Display the response
        st.subheader("Response : ")
        st.write(response)
    else:
        st.warning("Please provide both a question and an image.")

