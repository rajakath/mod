import streamlit as st
from openai import OpenAI
import json

# Function to serialize the output
def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string

# Access the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai_secret"]

# Initialize the OpenAI client with the API key from secrets
client = OpenAI(api_key="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")

# Streamlit UI components
st.title("OpenAI Moderation API Demo")

user_input = st.text_area("Enter text to moderate")

if st.button('Moderate'):
    response = client.moderations.create(input=user_input)
    output = response.results[0]
    serialized_output = serialize(output)
    json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)
    st.json(json_output)