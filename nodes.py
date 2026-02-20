import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from datetime import datetime
from state import AuditorState

def configure_gemini():
    """
    Ensures Gemini is configured with a valid key before any node runs.
    """
    # 1. Try environment variable (local)
    api_key = os.environ.get("GEMINI_API_KEY")

    # 2. Try Streamlit secrets (cloud)
    if not api_key:
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass

    if not api_key:
        raise ValueError("No API Key found. Please check Streamlit Secrets.")

    # .strip() handles hidden spaces, configure() sets it for the session
    genai.configure(api_key=api_key.strip())

# We use the full model path for maximum compatibility
MODEL_NAME = 'models/gemini-1.5-flash'

# --- REAL AI NODES ---

def extraction_node(state: AuditorState):
    print("--- NODE: EXTRACTION ---")
    try:
        configure_gemini() # Ensure key is set right before use
        model = genai.GenerativeModel(MODEL_NAME)
        img = Image.open(state["image_path"])
        
        prompt = "Identify Retailer and Purchase Date (YYYY-MM-DD). Format: Retailer: [Name], Date: [Date]"
        response = model.generate_content([prompt, img])
        
        return {
            "retailer": response.text.strip(), 
            "logs": ["AI successfully extracted data from receipt."]
        }
    except Exception as e:
        return {"logs": [f"Extraction failed: {str(e)}"]}

def research_node(state: AuditorState):
    print("--- NODE: RESEARCH ---")
    try:
        configure_gemini()
        model = genai.GenerativeModel(MODEL_NAME)
        retailer = state.get("retailer", "IKEA")
        
        prompt = f"Summarize official return policy for {retailer}. Focus on window and opened/unopened rules."
        response = model.generate_content(prompt)
        
        return {
            "raw_policy_text": response.text,
            "logs": [f"Retrieved policy knowledge for {retailer}."]
        }
    except Exception as e:
        return {"logs": [f"Research failed: {str(e)}"]}

def auditor_node(state: AuditorState):
    print("--- NODE: AUDIT ---")
    try:
        configure_gemini()
        model = genai.GenerativeModel(MODEL_NAME)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        policy = state.get("raw_policy_text", "No policy found.")
        facts = state.get("retailer", "No retailer found.")

        prompt = f"Today: {current_date}. Context: {facts}. Policy: {policy}. Can I return it? VERDICT and PLAN."
        response = model.generate_content(prompt)
        
        return {
            "audit_report": response.text,
            "logs": ["Audit complete based on policy math."]
        }
    except Exception as e:
        return {"audit_report": f"Audit failed: {str(e)}", "logs": ["Audit error."]}
