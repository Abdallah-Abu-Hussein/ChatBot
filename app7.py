from dotenv import load_dotenv
import os
import json
import streamlit as st

load_dotenv()

## Initialize Google GenerativeAI module
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

prompt_template = """You are an expert HR bot and your goal is to answer a question by Data.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {Name} with Id number {ID}, his/her position is {Position}, he/she has {Age} old, and his contract duration for {Contract}
Question: tell me all information about {Name}

Only return the correct answer, If you don't know the answer just say that you don't know, don't try to make up an answer.
Helpful answer:
"""

file_path = "/home/mrt/my_learning/ChatBot/Data/employees.json"

# Function to load data from JSON file
def load_data_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Load data from JSON file
data = load_data_from_json(file_path)

def get_gemini_response(question, employee_info):
    # Incorporate employee information into the question prompt
    prompt_with_context = prompt_template.format(**employee_info)
    response = chat.send_message(prompt_with_context + question, stream=True)
    response.resolve()  # Resolve the response before accessing attributes
    return response

## Initialize Streamlit app
st.image('Bayanat.png')  # Make sure 'Bayanat.png' is in the correct location or provide the correct path
st.markdown("<h1 style='text-align: center; color: red;'>شركة بيانات الرقمية</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: green;'>LLM Application</h2>", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Define prompt options dynamically based on employee names
prompt_options = [employee['Name'] for employee in data]

# Add prompt selector
selected_prompt = st.selectbox("Select an employee name:", prompt_options)

input_text = st.text_area("Question:", key='input')

# Use the selected prompt if input is empty
if not input_text and selected_prompt:
    # Retrieve employee information based on selected employee's name
    employee_info = next((employee for employee in data if employee['Name'] == selected_prompt), None)
    if employee_info:
        input_text = prompt_template.format(**employee_info)

submit_button = st.button("Ask the question :white_check_mark: " )

if submit_button and input_text:
    # Retrieve employee information based on selected employee's name
    employee_info = next((employee for employee in data if employee['Name'] == selected_prompt), None)
    if employee_info:
        response = get_gemini_response(input_text, employee_info)
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response:
            if isinstance(chunk, str):
                st.write(chunk)
            else:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))

# If you want a chat history just uncomment the line.
#st.subheader("The Chat history is")
#for role, text in st.session_state['chat_history']:
#    st.write(f"{role}: {text}")

st.markdown("<h5 style='text-align: center; color: red;'> Founded by Tariq Ibrahim </h5>", unsafe_allow_html=True)
print("ChatBot ready to use ✓")
