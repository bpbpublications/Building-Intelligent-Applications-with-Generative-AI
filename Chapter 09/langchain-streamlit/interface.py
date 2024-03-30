import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent

def decode_response(response: str) -> dict:
    """ This function converts the string response from the model to a dictionary.
    Args:
        response (str): The string response from the model.
    Returns:
        dict: The dictionary representation of the response.
    """
    response_dict = json.loads(response)
    return response_dict

def write_response(response_dict: dict):
    """ This function writes the response from the model to the Streamlit app.
    Args:
        response_dict (dict): The dictionary representation of the response.
    """
    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)
        
    # Check if the response is a table. 
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

query = st.text_area("Type your query here")

if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(data)

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)
    print(decoded_response)

    # Write the response to the Streamlit app.
    write_response(decoded_response)