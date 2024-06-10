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
st.markdown("""
    <style>
    .main {
        background-image: url("https://cdn.wallpapersafari.com/0/62/TA4eir.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        padding: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        font-size: 16px;
    }
    .chat-history {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        max-height: 400px;
        overflow: auto;
        margin-top: 20px;
    }
    .chat-entry {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-message {
        background-color: #e6f7ff;
        color: #005b96;
        text-align: left;
    }
    .bot-message {
        background-color: #005b96;
        color: #ffffff;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Career Counseling Chat Application")

# Use a form for input and button
with st.form(key='my_form'):
    user_question = st.text_input("Ask a question about career counseling:", key="user_input")
    submit_button = st.form_submit_button(label='Submit')

# Check if the form is submitted
if submit_button and user_question:
    # Get the response from Gemini Pro
    answer = LLM_Response(user_question)
    # Append the question and answer to the chat history
    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Career Hub", answer))

# Iterate over the chat history list to show each question followed by its answer
chat_history_html = '<div class="chat-history">'
for i in range(len(st.session_state.chat_history) - 1, -1, -2):
    if i - 1 >= 0:
        question_speaker, question_message = st.session_state.chat_history[i - 1]
        answer_speaker, answer_message = st.session_state.chat_history[i]
        
        chat_history_html += f"""
        <div class="chat-entry user-message"><b>{question_speaker}:</b> {question_message}</div>
        <div class="chat-entry bot-message"><b>{answer_speaker}:</b> {answer_message}</div>
        """
# Close the div tag for the chat history section
chat_history_html += "</div>"

# Display the chat history
st.markdown(chat_history_html, unsafe_allow_html=True)
