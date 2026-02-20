import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from datetime import datetime
from state import AuditorState

# --- 1. API Configuration (Environment Aware) ---
API_KEY = os.environ.get("GEMINI_API_KEY") 

# If we are on the web (Streamlit Cloud), this will work.
# If we are local, the 'try' block prevents the crash you just saw.
if not API_KEY:
    try:
        if "GEMINI_API_KEY" in st.secrets:
            API_KEY = st.secrets["GEMINI_API_KEY"]
    except:
        # We are local and no export was found
        pass

if not API_KEY:
    # Key will be pulled from Streamlit Secrets on the web
    API_KEY = ""

genai.configure(api_key=API_KEY)

# Use the alias that worked in our diagnostic
MODEL_NAME = 'models/gemini-flash-latest'

# --- 2. Real AI Nodes (Quota-Optimized) ---

def extraction_node(state: AuditorState):
    """Task: Identify Brand and Date from the photo"""
    print("--- NODE: REAL EXTRACTION ---")
    model = genai.GenerativeModel(MODEL_NAME)
    img = Image.open(state["image_path"])
    
    prompt = "Extract the Retailer name and Purchase Date (YYYY-MM-DD) from this receipt. Return ONLY those two facts."
    
    response = model.generate_content([prompt, img])
    text = response.text.strip()
    
    return {
        "retailer": text, 
        "logs": [f"AI extracted facts: {text}"]
    }

def research_node(state: AuditorState):
    """Task: Retrieve policy from Internal Knowledge (Bypasses Search Quota)"""
    print("--- NODE: KNOWLEDGE RESEARCH ---")
    model = genai.GenerativeModel(MODEL_NAME)
    
    retailer = state.get("retailer", "the retailer on the receipt")
    
    # We ask the LLM to use its internal knowledge instead of the Search Tool
    prompt = f"""
    You are an expert on consumer rights. Based on your internal knowledge, 
    what is the official return policy for {retailer}? 
    
    Please provide:
    1. The return window (number of days).
    2. Any nuances (opened vs unopened).
    3. Any specific exclusions.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "raw_policy_text": response.text,
        "logs": [f"Retrieved {retailer} policy from internal knowledge base."]
    }

def auditor_node(state: AuditorState):
    """Task: Final Reasoning & Date Math"""
    print("--- NODE: REAL AUDIT ---")
    model = genai.GenerativeModel(MODEL_NAME)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    policy = state.get("raw_policy_text", "")
    receipt_facts = state.get("retailer", "")

    prompt = f"""
    Today's Date: {current_date}
    Receipt Data: {receipt_facts}
    Policy Details: {policy}
    
    TASK:
    Analyze if the user can return the item. 
    1. Calculate days elapsed.
    2. Compare against the policy.
    3. Provide a VERDICT and a brief LOGISTICS PLAN.
    """
    
    response = model.generate_content(prompt)
    
    return {
        "audit_report": response.text,
        "logs": ["Performed cross-reference audit and date math."]
    }