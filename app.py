import streamlit as st
from sql_agent import full_chain
import warnings

warnings.filterwarnings("ignore")


st.header(body='Text-to-SQL LLM App')
st.divider()

# Initialize Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Replicating the history
for message in st.session_state["messages"]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Creating Prompt and Response input outputs
if prompt := st.chat_input("Ask a question to the database"):
    st.chat_message("user").markdown(prompt)
    st.session_state['messages'].append({
        "role": "user",
        "content": f"{prompt}",
    })
    with st.status("Making LLM Call", state="running") as status:
        response = full_chain.invoke({"question": f"{prompt}"})
        status.update(label="Received Response!", state="complete")
    st.chat_message("ai").markdown(response)
    st.session_state['messages'].append({
        "role": "assistant",
        "content": f"{response}",
    })
    
    
