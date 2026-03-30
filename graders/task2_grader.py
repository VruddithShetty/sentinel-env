def grade_task2(response: str) -> float:
    response = response.lower()
    if "anomaly" in response or "unrecognized process" in response:
        return 1.0
    return 0.0
