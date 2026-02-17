import operator
from typing import Annotated, TypedDict, List, Optional

class AuditorState(TypedDict):
    """
    The 'Memory' of our Senior Co-worker Auditor.
    """
    # 1. Input data
    image_path: str
    
    # 2. Extracted facts (filled by the Extractor Node)
    retailer: Optional[str]
    purchase_date: Optional[str]
    items: List[str]
    
    # 3. Research data (filled by the Researcher Node)
    raw_policy_text: Optional[str]
    
    # 4. Final output (filled by the Auditor Node)
    audit_report: Optional[str]
    
    # 5. The Verification Trace / Internal Logs
    # Using Annotated and operator.add tells LangGraph to 
    # append new logs to the list rather than overwriting them.
    logs: Annotated[List[str], operator.add]