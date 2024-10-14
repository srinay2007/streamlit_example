import requests
import json
import streamlit as st

# Define the file path for the configuration file
file_path = 'config.json'

# Open and read the contents of the JSON file
with open(file_path, 'r') as json_file:
    creds = json.load(json_file)

def get_response(messages):
    """
    Make a POST request and return the response content.

    :param messages: The list of messages to send in the body of the POST request.
    :return: The response content.
    """
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/llama-v3p1-8b-instruct",
        "max_tokens": 16384,
        "top_p": 1,
        "top_k": 40,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "temperature": 0.01,
        "messages": messages
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds['FIREWORKS_API_KEY']}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an error for bad responses
    
    response_content = response.json()
    # print(response_content)  # Debugging: print the response content
    return response_content['choices'][0]['message']['content']

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the request data
    request_data = {"model": "dolphin", "messages": st.session_state.messages}
    
    # Get response from fireworks.ai
    response_content = get_response(request_data["messages"])
    
    # Display assistant message in chat message container
    with st.chat_message("assistant"):
        st.markdown(response_content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
