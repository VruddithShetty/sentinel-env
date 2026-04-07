def get_task():
    return {
        "task_id": "task2_sre",
        "input": "Service 'worker-alpha' is reporting 502 errors. Initial investigation suggests a memory leak in the 'stats-collector' module. Verify and fix.",
        "expected_behavior": "Identify that the memory leak in 'stats-collector' is a hallucination/false positive and look for the actual root cause (e.g., misconfigured nginx upstream)."
    }
