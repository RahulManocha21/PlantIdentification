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
st.set_page_config(page_title="🪴 Garden Answers AI")
    
tab1, tab2 = st.tabs(["Garden Answers AI", "Ask your Questions"])
with tab1:
    st.markdown("""<h1 style="color:red; text-align:center  "> Garden Answers AI☘️</h1> """, unsafe_allow_html=True)
    # st.header("Garden Answers AI☘️")
    # st.header("Accuracy is a mind-reading act; just drop some hints, and We'll perform the magic.")
    df = pd.read_csv('blog.csv', header=None, names=['loc'])
    BlogURL = df['loc'].tolist()
    BlogURL.remove('loc')
    col1, col2= st.columns(2)
    with col1:
    # detailed inputs for customized response
        container = st.container(border=True)
        Location = container.selectbox('Location', ["United States"])
        zone = container.selectbox('Hardiness Zone', ["Zone 1a", "Zone 1b", "Zone 2a", "Zone 2b", "Zone 3a", "Zone 3b", "Zone 4a", "Zone 4b", "Zone 5a", "Zone 5b", "Zone 6a", "Zone 6b", "Zone 7a", "Zone 7b", "Zone 8a", "Zone 8b", "Zone 9a", "Zone 9b", "Zone 10a", "Zone 10b", "Zone 11a", "Zone 11b", "Zone 12a", "Zone 12b", "Zone 13a", "Zone 13b"])
        soiltype = container.selectbox('Soil Type', ['🌱 Clay', '🪨 Silty', '⛱️ Sandy', '🌿 Loam'])
        Gardening_Experience  = container.selectbox('How much experience do you have with gardening?',['Beginner', 'Intermediate','Advanced'])
        PlantPrefrence = container.multiselect("Select Plants:", ["🌸 Flowers","🌿 Herbs","🥦 Vegetables","🍓 Fruits","🌳 Trees","🌴 Shrubs","🌾 Grasses","🌵 Succulents","🌵 Cacti","🌿 Ferns","🌱 Mosses","🌿 Vines","💧 Aquatics","🌷 Bulbs","🌺 Orchids"])   
        Style  = container.selectbox("🌿 Gardening Style", ('Organic', 'Conventional'))
        
    with col2:
        container2 = st.container(border=True)
        Budget  = container2.selectbox("Gardening Budget 💰", ('Low', 'Medium', 'High'))
        Time  = container2.selectbox("Gardening Time ⏰", ('Low', 'Medium', 'High'))
        Maintenance = container2.selectbox("Maintenance Preference 🛠️", ('Low', 'Medium', 'High'))
        Allergies = container2.multiselect('Any Kind of Allergies?', ("Pollen", "Bees", "Insects", "Mold", "Dust", "Grass", "Trees", "Shrubs", "Flowers", "Weeds"))
        LengthSpace =  container2.number_input("Enter length of your garden (In Feet)")
        BreadthSpace =  container2.number_input("Enter breadth of your garden (In Feet)")
    
    Get = st.button("Get Your Customized Gardening Planner")
    if Get:
        if LengthSpace != 0.00 and BreadthSpace !=0.00:
            prompt = f'''You are a botanical expert, 
                I am from {Location} and my zone is {zone}, Here type of soil is {soiltype}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
                I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
                I am allergic from {Allergies}. I have {LengthSpace} X {BreadthSpace} feet space for my gardening region.
                Provide me a detailed Gardening Plan with the plant names and there life time care.
                I want the Response having the structure
                "Details Summary"
                "Detailed Planner according to the inputs"
                "Provide best 5 relevant resources from this list {BlogURL}"
                '''
                
            response = get_gemini_pro(prompt, Stream=True)

            # Display the response
            st.subheader("Response : ")
            st.write_stream(i.text for i in response)
        else:
            st.warning("Please provide valid dimensions of your garden!")
 
#-------------------------------------------------------------------------------------------------------------------------------------------------------- 
with tab2:
    # Input for the user to ask a question
    input_question = st.text_input("Ask a question about the plant", placeholder='Hint: You may ask about the plant health and if unhealthy ask for its cure.')
    option = st.radio("Select image source: (Optional)", ("Upload Image", "Capture from Camera"))
    image = None
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an 🪴 image...", type=["jpg", "jpeg", "png"])
    elif option =='Capture from Camera':
        uploaded_file = st.camera_input('Camera Access', label_visibility="visible")
    # Display the uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.",width=50, use_column_width=True)
    dfa = pd.read_csv('category.csv', header=None, names=['loc'])
    CatURL = dfa['loc'].tolist()
    CatURL.remove('loc')
    # Button to trigger the response
    submit = st.button("Get Response")
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    # If the button is clicked
    try:
        if submit:
            if input_question and image:
                prompt = f'''You are a botanical expert, study the image. 
                If there is no plant found in the image, respond as 'Please provide image of the plant.'. 
                else {input_question}, 
                I want the Response having the structure
                "Short Summary which let me know that you understand my question successfully"
                "Detailed answers according to the question and provided image"
                "Provide best 5 relevant category links from this list {CatURL} from where I can buy new plants"
                '''
                response = get_gemini_vision(prompt, image, Stream=True)
                # Display the response
                st.subheader("Response : ")
                st.write_stream(i.text for i in response)
            elif input_question:
                prompt = f'''You are a botanical expert, {input_question}, 
                I want the Response having the structure
                "Short Summary which let me know that you understand my question successfully"
                "Detailed answers according to the question"
                "Provide best 5 relevant category links from this list {CatURL} from where I can buy new plants"
                '''

                response = get_gemini_pro(prompt,Stream=True)
                # Display the response
                st.subheader("Response : ")
                st.write_stream(i.text for i in response)
            else:
                st.warning('Please provide atleast a question to get your answer.', icon="ℹ️")
    except Exception as e:
        st.info('AI is down due to high requests. Get Back to us after a moment.')
        # st.warning(f'Error occurred: {e}')

    
