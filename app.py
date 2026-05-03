import streamlit as st
import requests

st.set_page_config(page_title="Police Rulebook Assistant", page_icon="👮", layout="wide")

API_URL = "http://localhost:8000"

st.title("👮 Police Rulebook Assistant")
st.caption("RAG Document Assistant for SOPs, Complaint Manuals & Citizen Procedures")

with st.sidebar:
    st.header("📁 Knowledge Base Management")
    
    uploaded_file = st.file_uploader("Upload Police Document (PDF)", type=["pdf"])
    
    if uploaded_file:
        if st.button("📤 Upload to Knowledge Base"):
            with st.spinner("Processing document..."):
                files = {"file": uploaded_file}
                response = requests.post(f"{API_URL}/upload", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ {result['message']}")
                    st.info(f"Created {result['chunks_created']} text chunks")
                else:
                    st.error(f"Upload failed: {response.text}")
    
    st.divider()
    st.caption("📌 **Sample Questions to Ask:**")
    st.caption("• How to file a complaint?")
    st.caption("• What is the procedure for?")
    st.caption("• Tell me about citizen rights")
    
    st.divider()
    try:
        status = requests.get(f"{API_URL}/status").json()
        st.success(f"✅ Status: {status['status']}")
        st.info(f"📄 Documents loaded: {status['documents_loaded']}")
    except:
        st.error("❌ Backend not running")

st.header("💬 Ask Questions from Police Rulebook")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            st.caption(f"📚 Source: {', '.join(message['sources'])}")

if prompt := st.chat_input("Ask a question about police procedures..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching police rulebook..."):
            try:
                response = requests.post(f"{API_URL}/ask", json={"query": prompt})
                if response.status_code == 200:
                    result = response.json()
                    st.markdown(result["answer"])
                    if result["sources"]:
                        st.caption(f"📚 Source: {', '.join(result['sources'])}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"]
                    })
                else:
                    st.error(f"Error: {response.text}")
            except:
                st.error("❌ Cannot connect to backend")

st.divider()
st.caption("🏆 **Project PRJ-005** | Police Rulebook Assistant | Week 1 Complete ✅")