import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import time
import pandas as pd

genai.configure(api_key=st.secrets["SecretKey"]["GOOGLE_API_KEY"])

def get_gemini_vision(input, image, Stream):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image], stream=Stream)
    return response

def get_gemini_pro(input, Stream):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input, stream=Stream)
    return response

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# initialize our streamlit app
st.set_page_config(page_title="🪴 Plant Pulse Pro")
st.header("Plant Pulse Pro ☘️")
info_check = st.toggle('Precision on demand – just flip the switch for an information upgrade.')
image_choice = st.toggle("Do u have any plant image to share")
if info_check:
    # detailed inputs for customized response
    st.sidebar.header("Accuracy is a mind-reading act; just drop some hints, and We'll perform the magic.")
    Location = st.sidebar.selectbox('Location', ["United States"])
    zone = st.sidebar.selectbox('Hardiness Zone', ["Zone 1a", "Zone 1b", "Zone 2a", "Zone 2b", "Zone 3a", "Zone 3b", "Zone 4a", "Zone 4b", "Zone 5a", "Zone 5b", "Zone 6a", "Zone 6b", "Zone 7a", "Zone 7b", "Zone 8a", "Zone 8b", "Zone 9a", "Zone 9b", "Zone 10a", "Zone 10b", "Zone 11a", "Zone 11b", "Zone 12a", "Zone 12b", "Zone 13a", "Zone 13b"])
    soiltype = st.sidebar.selectbox('Soil Type', ['🌱 Clay', '🪨 Silty', '⛱️ Sandy', '🌿 Loam'])
    Gardening_Experience  = st.sidebar.selectbox('How much experience do you have with gardening?',['Beginner', 'Intermediate','Advanced'])
    PlantPrefrence = st.sidebar.multiselect("Select Plants:", ["🌸 Flowers","🌿 Herbs","🥦 Vegetables","🍓 Fruits","🌳 Trees","🌴 Shrubs","🌾 Grasses","🌵 Succulents","🌵 Cacti","🌿 Ferns","🌱 Mosses","🌿 Vines","💧 Aquatics","🌷 Bulbs","🌺 Orchids"])   
    Style  = st.sidebar.selectbox("🌿 Gardening Style", ('Organic', 'Conventional'))
    Budget  = st.sidebar.selectbox("Gardening Budget 💰", ('Low', 'Medium', 'High'))
    Time  = st.sidebar.selectbox("Gardening Time ⏰", ('Low', 'Medium', 'High'))
    Maintenance = st.sidebar.selectbox("Maintenance Preference 🛠️", ('Low', 'Medium', 'High'))
    Allergies = st.sidebar.multiselect('Any Kind of Allergies?', ("Pollen", "Bees", "Insects", "Mold", "Dust", "Grass", "Trees", "Shrubs", "Flowers", "Weeds"))
    LengthSpace =  st.sidebar.number_input("Enter length of your garden (In Feet)")
    BreadthSpace =  st.sidebar.number_input("Enter breadth of your garden (In Feet)")
else:
    Location = None

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# Input for the user to ask a question
input_question = st.text_input("Ask a question about the plant", placeholder='Hint: You may ask about the plant health and if unhealthy ask for its cure.')
if image_choice: 
    option = st.radio("Select image source:", ("Upload Image", "Capture from Camera"))
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an 🪴 image...", type=["jpg", "jpeg", "png"])
    elif option =='Capture from Camera':
        uploaded_file = st.camera_input('Camera Access', label_visibility="visible")
    # Display the uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
else:
    image = None

URL = pd.read_csv('category.csv')
# st.dataframe(URL)
# Button to trigger the response
submit = st.button("Get Response")
#--------------------------------------------------------------------------------------------------------------------------------------------------------
# If the button is clicked
if submit:
    if input_question and Location and image:
        prompt = f'''You are a botanical expert, study the image and respond accordingly. 
        If there is no plant in the image, respond as No plant found. else
        I am from {Location} and my zone is {zone}, Here type of soil is {soiltype}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}. I have {LengthSpace} X {BreadthSpace} feet space for my gardening region.
        {input_question}, 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_vision(prompt, image, Stream=True)

        # Display the response
        st.subheader("Response : ")
        st.write_stream(i.text for i in response)

    elif input_question and Location:
        prompt = f'''You are a botanical expert,
        I am from {Location} and my zone is {zone}, Here type of soil is {soiltype}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}. I have {LengthSpace} X {BreadthSpace} feet space for my gardening region.
        {input_question}, 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_pro(prompt, Stream=True)
        # Display the response
        st.subheader("Response : ")
        st.write_stream(i.text for i in response)
        

    elif image and Location:
        prompt = f'''You are a botanical expert, study the image and respond accordingly. 
        If there is no plant in the image, respond as No plant found. else
        I am from {Location} and my zone is {zone}, Here type of soil is {soiltype}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}.  I have {LengthSpace} X {BreadthSpace} feet space for my gardening region.
        Suggest me can i grow the product shown in image. 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_vision(prompt, image, Stream=True)

        # Display the response
        st.subheader("Response : ")
        st.write_stream(i.text for i in response)
    
    elif input_question:
        prompt = f'''You are a botanical expert,
        {input_question}, 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_pro(prompt, Stream=True)
        # Display the response
        st.subheader("Response : ")
        st.write_stream(i.text for i in response)

    elif image:
        prompt = f'''You are a botanical expert, study the image and respond accordingly. 
        If there is no plant in the image, respond as No plant found. else
        Provide information about the plant shown in the image.
        Suggest me can i grow the product shown in image. 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_vision(prompt, image, Stream=True)

        # Display the response
        st.subheader("Response : ")
        st.write_stream(i.text for i in response)

    else:
        st.warning("Please provide atleast a question or an image.")
    
    matchedURL = []
    if image:
        prompt = """You are a botanical expert, study the image,
         If there is no plant in the image, respond as No plant found.
        else tell me in 1 words from which category the plant in the image belongs to"""
        time.sleep(2)
        Product_category = get_gemini_vision(prompt, image, Stream=False)
        st.subheader('Product Which You May Like')
        for i in URL['loc']:
            if Product_category.text.replace('.','').lower().strip() in i.lower():
                matchedURL.append(i)

    elif input_question:
        prompt = f"""You are a botanical expert, study the user input, the input is 
        {input_question}. You have to tell me more relevant only 1 plant we can suggest to the user to buy
        provide your answer in only 1 word"""
        time.sleep(2)
        Product_category = get_gemini_pro(prompt, Stream=False)
        st.subheader('Product Which You May Like')
        for i in URL['loc']:
            if Product_category.text.replace('.','').lower().strip() in i.lower():
                matchedURL.append(i)
    
    if matchedURL:
        st.write(Product_category.text)
        st.write(f'Buy your Favourite gardens decor or plants from the reliable Web Stores {matchedURL}')
    else:
        st.write('No Match')

