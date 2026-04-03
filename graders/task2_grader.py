def grade_task2(response: str) -> float:
    """
    Task 2: Cascading Failure (Medium)
    Expected: Detect anomaly timing (08:10), stop execution, escalate to SRE.
    """
    response = response.lower()
    score = 0.0
    
    # 1. Critical Timing Detection (Critical) - 0.50 max
    if "08:10" in response and ("anomaly" in response or "unrecognized" in response):
        score += 0.50
    elif "anomaly" in response:
        score += 0.30 # Found anomaly but missed time (08:10)
    else:
        score -= 0.50 # Complete failure to detect
        
    # 2. Operational Control (Nuance) - 0.25 max
    if any(term in response for term in ["escalate", "notify", "on-call", "alert", "report"]):
        score += 0.25
    else:
        score -= 0.15 # Weak on operational incident response
        
    # 3. Halt/Safeguard action (Nuance) - 0.15 max
    if any(term in response for term in ["stop", "halt", "shutdown", "quarantine", "blocking"]):
        score += 0.15
    else:
        score -= 0.10 # Weak on risk mitigation
        
    # 4. Contextual Analysis (Nuance) - 0.10 max
    if any(term in response for term in ["system", "log", "security", "impact", "failure"]):
        score += 0.10
    else:
        score -= 0.05
        
    return round(max(0.0, min(1.0, score)), 2)
