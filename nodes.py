from state import AuditorState

def extraction_node(state: AuditorState):
    """
    MOCK: In Phase 4, this will use Gemini Vision.
    """
    print("\n[NODE] Extractor: Analyzing receipt image...")
    
    # We are simulating a successful extraction
    return {
        "retailer": "IKEA",
        "purchase_date": "2026-01-25",
        "items": ["GRÖNLID Sofa", "As-Is Lightbulb"],
        "logs": ["Verified brand: IKEA from logo.", "Extracted date: 2026-01-25."]
    }

def research_node(state: AuditorState):
    """
    MOCK: In Phase 4, this will use the Google Search tool.
    """
    retailer = state.get("retailer", "Unknown")
    print(f"[NODE] Researcher: Searching for {retailer} policy...")
    
    # Simulating a found policy
    policy_text = "IKEA Policy: 365 days unopened, 180 days opened. As-Is items are final sale."
    
    return {
        "raw_policy_text": policy_text,
        "logs": [f"Retrieved live policy for {retailer} via mock search."]
    }

def auditor_node(state: AuditorState):
    """
    MOCK: In Phase 4, this will use Gemini Reasoning.
    """
    print("[NODE] Auditor: Cross-referencing receipt against policy...")
    
    # Simulating the high-stakes reasoning
    report = """
    VERDICT: Conditional Approval.
    PLAN: Return sofa within 180 days (opened) or 365 (unopened).
    WARNING: The Lightbulb is 'As-Is' (Final Sale).
    """
    
    return {
        "audit_report": report,
        "logs": ["Performed date math: 23 days elapsed. Applied 'As-Is' exclusion."]
    }