def grade_task2(response: str) -> float:
    """
    Task 2: Cascading Failure (Medium)
    Input: system logs with anomaly.
    Expected: Detect anomaly timing (08:10), stop execution, escalate.
    """
    response = response.lower()
    score = 0.0
    
    # 1. Detection of anomaly at correct timestamp (Critical)
    if "08:10" in response and ("anomaly" in response or "unrecognized" in response):
        score += 0.5
    elif "anomaly" in response:
        score += 0.3 # Found anomaly but missed time
    else:
        score -= 0.5
        
    # 2. Stop/Escalate action
    if any(term in response for term in ["escalate", "notify", "stop", "halt", "alert"]):
        score += 0.3
    else:
        score -= 0.2
        
    # 3. Reasoning and Impact Analysis
    if any(term in response for term in ["security", "risk", "failure", "impact", "logs"]):
        score += 0.2
    else:
        score -= 0.2
        
    return round(max(0.0, min(1.0, score)), 2)
