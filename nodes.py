import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from datetime import datetime
from state import AuditorState

# --- 1. API Configuration (Defensive) ---
raw_key = os.environ.get("GEMINI_API_KEY") 

if not raw_key:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            raw_key = st.secrets["GEMINI_API_KEY"]
    except:
        pass

# IMPORTANT: .strip() removes hidden spaces/newlines that cause InvalidArgument
API_KEY = raw_key.strip() if raw_key else None

if API_KEY:
    genai.configure(api_key=API_KEY)

# Use the most stable naming convention for the Cloud environment
MODEL_NAME = 'gemini-1.5-flash' 

# --- 2. Real AI Nodes ---

def extraction_node(state: AuditorState):
    """Task: Identify Brand and Date from the photo"""
    print("--- NODE: REAL EXTRACTION ---")
    
    # Safety check: Ensure the image file exists
    if not os.path.exists(state["image_path"]):
        return {"logs": ["Error: Image file not found on server."]}

    model = genai.GenerativeModel(MODEL_NAME)
    img = Image.open(state["image_path"])
    
    prompt = "Extract Retailer name and Purchase Date (YYYY-MM-DD). Format: Retailer: [Name], Date: [Date]"
    
    # We pass the prompt and image as a list
    try:
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        return {
            "retailer": text, 
            "logs": [f"AI successfully analyzed image."]
        }
    except Exception as e:
        return {"logs": [f"Extraction failed: {str(e)}"]}

def research_node(state: AuditorState):
    """Task: Knowledge Research"""
    print("--- NODE: KNOWLEDGE RESEARCH ---")
    model = genai.GenerativeModel(MODEL_NAME)
    retailer = state.get("retailer", "IKEA")
    
    prompt = f"Summarize official return policy for {retailer}. Focus on window and opened/unopened rules."
    
    try:
        response = model.generate_content(prompt)
        return {
            "raw_policy_text": response.text,
            "logs": [f"Retrieved policy knowledge."]
        }
    except Exception as e:
        return {"logs": [f"Research failed: {str(e)}"]}

def auditor_node(state: AuditorState):
    """Task: Final Reasoning"""
    print("--- NODE: REAL AUDIT ---")
    model = genai.GenerativeModel(MODEL_NAME)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    policy = state.get("raw_policy_text", "No policy found.")
    facts = state.get("retailer", "No retailer found.")

    prompt = f"Today: {current_date}. Context: {facts}. Policy: {policy}. Can I return it? VERDICT and PLAN."
    
    try:
        response = model.generate_content(prompt)
        return {
            "audit_report": response.text,
            "logs": ["Audit complete."]
        }
    except Exception as e:
        return {"audit_report": f"Audit failed: {str(e)}", "logs": ["Audit error."]}
