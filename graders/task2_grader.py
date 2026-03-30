def grade_task2(response: str) -> float:
    response = response.lower()
    score = 0.0
    
    if "anomaly" in response or "unrecognized process" in response:
        score += 0.5
        
    if "08:10" in response or "early" in response:
        score += 0.3
    else:
        score -= 0.2
        
    if "log" in response or "detected" in response:
        score += 0.2
        
    reasoning_keywords = ["because", "reason", "due to", "security", "risk"]
    if not any(k in response for k in reasoning_keywords):
        score -= 0.15 # generic explanation penalty
        
    return round(max(0.0, min(1.0, score)), 2)
