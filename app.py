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
st.header("Plant Identification ☘️")
st.sidebar.header('Fill the Details to get the Customized Response')
Location = st.sidebar.selectbox('Location', ["United States"])
Gardening_Experience  = st.sidebar.selectbox('How much experience do you have with gardening?',['Beginner', 'Intermediate','Advanced'])
PlantPrefrence = st.sidebar.multiselect("Select Plants:", ["🌸 Flowers","🌿 Herbs","🥦 Vegetables","🍓 Fruits","🌳 Trees","🌴 Shrubs","🌾 Grasses","🌵 Succulents","🌵 Cacti","🌿 Ferns","🌱 Mosses","🌿 Vines","💧 Aquatics","🌷 Bulbs","🌺 Orchids"])   
Style  = st.sidebar.selectbox("🌿 Gardening Style", ('Organic', 'Conventional'))
Budget  = st.sidebar.selectbox("Gardening Budget 💰", ('Low', 'Medium', 'High'))
Time  = st.sidebar.selectbox("Gardening Time ⏰", ('Low', 'Medium', 'High'))
Maintenance = st.sidebar.selectbox("Maintenance Preference 🛠️", ('Low', 'Medium', 'High'))
Allergies = st.sidebar.multiselect('Any Kind of Allergies?', ("Pollen", "Bees", "Insects", "Mold", "Dust", "Grass", "Trees", "Shrubs", "Flowers", "Weeds"))
Space =  st.sidebar.number_input("Enter the available space for your garden (in square feet)")
# Input for the user to ask a question
input_question = st.text_input("Ask a question about the plant", placeholder='Hint: You may ask about the plant health and if unhealthy ask for its cure.')

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
    if image is not None and input_question is not None:
        input_text = f'''You are a botanical expert, study the image and respond accordingly. 
        If there is no plant in the image, respond as No plant found. else
        I am from {Location}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}. I have {Space} square feet space for my garden.
        {input_question}, 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_response(input_text, image)

        # Display the response
        st.subheader("Response : ")
        st.write(response)
    elif input_question is not None:
        input_text = f'''You are a botanical expert,
        I am from {Location}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}. I have {Space} square feet space for my garden.
        {input_question}, 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_response(input_text)

        # Display the response
        st.subheader("Response : ")
        st.write(response)
    elif image is not None:
        input_text = f'''You are a botanical expert, study the image and respond accordingly. 
        If there is no plant in the image, respond as No plant found. else
        I am from {Location}, I am at {Gardening_Experience} level in gardening, I want to have {PlantPrefrence} in my garden.
        I want to do in {Style} style gardening.  My budget is {Budget}, time is {Time} and Maintenance preference is {Maintenance}. 
        I am allergic from {Allergies}. I have {Space} square feet space for my garden.
        Suggest me can i grow the product shown in image. 
        Write your answer in layman's terms with less technicalities, so everyone can understand.'''
        
        response = get_gemini_response(input_text, image)

        # Display the response
        st.subheader("Response : ")
        st.write(response)
        
    else:
        st.warning("Please provide both a question and an image.")
