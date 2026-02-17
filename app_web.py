import streamlit as st
from main import app  # This imports your LangGraph State Machine
from PIL import Image
import os

# --- Page Config ---
st.set_page_config(page_title="Returnly", page_icon="⚖️", layout="wide")

st.title("⚖️ Returnly")
st.markdown("### I will tell you if that thing you bought can be returned.")

# --- Sidebar: Upload Evidence ---
st.sidebar.header("Evidence Upload")
uploaded_file = st.sidebar.file_uploader("Upload Receipt (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded receipt
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Receipt", use_container_width=True)
    
    # Save temporarily for the agent to read
    with open("temp_receipt.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.sidebar.button("Run Audit", use_container_width=True):
        with st.spinner("Agentic Orchestration in progress..."):
            # 1. Run the LangGraph Workflow
            initial_state = {
                "image_path": "temp_receipt.jpg",
                "logs": [],
                "items": []
            }
            
            # The Magic: Invoking your Graph
            final_state = app.invoke(initial_state)

            # 2. Display the Results in Two Columns
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("🔍 Verification Trace")
                st.info("Internal logic and policy cross-referencing:")
                for i, log in enumerate(final_state["logs"], 1):
                    st.write(f"**Step {i}:** {log}")

            with col2:
                st.subheader("📋 Final Logistics Plan")
                st.success(final_state["audit_report"])

else:
    st.info("Please upload a receipt image in the sidebar to begin the audit.")

# --- Footer ---
st.divider()
st.caption("Powered by Gemini 1.5 Flash & LangGraph | Returnly v1.0")
