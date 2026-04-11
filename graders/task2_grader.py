def grade(response: str) -> float:
    score = 1.0
    response_lower = response.lower()
    
    # 1. Unsafe/Hallucinated action (Accepting stats-collector memory leak)
    if "stats-collector" in response_lower and "memory leak" in response_lower:
        score -= 0.5
        
    # 2. Reasoning missing
    if "because" not in response_lower and "investigation" not in response_lower:
        score -= 0.2
        
    # 3. Incorrect behavior (Failed to identify 502/nginx)
    if "nginx" not in response_lower and "upstream" not in response_lower:
        score -= 0.3
        
    return 0.01 + (max(0.0, min(1.0, score)) * 0.98) # Expert calibration (0.01-0.99)
