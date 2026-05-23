import os
import streamlit as st
from PIL import Image
from agents import agent_app
from ingest import process_document

img = Image.open("test_icon.jpg")

st.set_page_config(page_title="PrivateSphere AI", page_icon=img, layout="centered")

st.markdown("""
<style>
    /* Target the default user avatar and force it to be blue */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #007BFF !important;
    }
    /* Ensure the icon inside it remains white for contrast */
    [data-testid="stChatMessageAvatarUser"] svg {
        fill: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("PrivateSphere: Privacy-First AI Agent")
st.subheader("Locally-hosted enterprise document analysis")

with st.sidebar:
    st.header("📁 Document Ingestion")
    uploaded_file = st.file_uploader("Upload a PDF to add to the local vector DB", type=["pdf"])
    
    if uploaded_file is not None:
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
            with st.spinner(f"Parsing and vectorizing {uploaded_file.name}..."):
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                process_document(uploaded_file.name)
                st.session_state.last_uploaded = uploaded_file.name
                
            st.success(f"Successfully indexed '{uploaded_file.name}'!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Agents are analyzing documents..."):
            try:
                active_file = st.session_state.get("last_uploaded", "")
                initial_state = {
                    "question": prompt, 
                    "filename": active_file,
                    "context": [], 
                    "answer": ""
                }
                
                final_state = agent_app.invoke(initial_state)
                response = final_state["answer"]
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error communicating with local agent graph: {e}")