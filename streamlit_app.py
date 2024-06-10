# from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as ggi

# Load environment variables
# load_dotenv(".env")

# Fetch the API key from the environment variables
# Ensure you securely manage and store your API keys
fetched_api_key = "AIzaSyDp17AjWrSCKyr35QYfIt6c2lZVHRJwyvY"  # Use os.getenv to fetch the API key

# Check if the API key was successfully fetched
if not fetched_api_key:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

# Configure the Gemini Pro API with the fetched API key
ggi.configure(api_key=fetched_api_key)

# Initialize the Gemini Pro generative model
model = ggi.GenerativeModel("gemini-pro")
chat = model.start_chat()

# Initialize session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to send a question to the LLM and receive a response
def LLM_Response(question):
    # Predefine the context for career counseling in Pakistan
    career_counseling_context = "Considering career counseling in Pakistan, "
    # Concatenate the context with the user's question
    full_question = career_counseling_context + question
    try:
        # Send the full question to Gemini Pro and stream the response
        response = chat.send_message(full_question, stream=True)
        # Convert response to a single string for easier handling
        full_response = ''.join([word.text for word in response])
    except Exception as e:
        full_response = "An error occurred: " + str(e)
    return full_response

# Streamlit UI components
st.title("Career Counseling Chat Application")

# Input field for the user's question
user_question = st.text_input("Ask a question about career counseling:", key="user_input")

# Button to submit the question and update chat history
def update_chat_history():
    if user_question:  # Check if there is a question
        # Get the response from Gemini Pro
        answer = LLM_Response(user_question)
        # Append the question and answer to the chat history
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("Career Hub", answer))
        # Clear the input box for the next question, use a workaround to reset
        st.session_state.user_input = ''
        st.experimental_rerun()  # Rerun the script to reset the input box

btn = st.button("Submit", on_click=update_chat_history)

# Set the background image for the chat section
background_image = "https://cdn.wallpapersafari.com/0/62/TA4eir.jpg"

# Using HTML and CSS to set the background image with improved coverage and positioning
chat_history_html = f"""
<style>
.chat-history {{
background-image: url({background_image});
background-size: cover;
background-repeat: no-repeat;
background-position: center;
padding: 50px;
border-radius: 10px;
overflow: auto;
max-height: 400px;
color: #f5f5f5;
}}
</style>
<div class="chat-history">
"""

# Iterate over the chat history list to show each question followed by its answer
for i in range(len(st.session_state.chat_history) - 1, -1, -2):
    if i - 1 >= 0:
        question_speaker, question_message = st.session_state.chat_history[i - 1]
        answer_speaker, answer_message = st.session_state.chat_history[i]
        
        chat_history_html += f"<p><b style='color: black; background-color: white;'>{question_speaker}:</b> <span style='color: black; background-color: white;'>{question_message}</span></p>"
        chat_history_html += f"<p><b style='color: white; background-color: black;'>{answer_speaker}:</b> <span style='color: white; background-color: black;'>{answer_message}</span></p>"

# Close the div tag for the chat history section
chat_history_html += "</div>"

# Display the chat history with the background image
st.markdown(chat_history_html, unsafe_allow_html=True)
