def get_task():
    return {
        "task_id": "task2_sre",
        "description": "Distributed System Triage",
        "difficulty": "Medium",
        "input": """INCIDENT REPORT: [P2] High Error Rate on 'gateway-prod'
LOG EXCERPT:
2026-04-11T08:50:01 gateway-prod [ERROR] upstream_reset_before_response_header
2026-04-11T08:50:03 gateway-prod [INFO] memory_usage=42% cpu=12%
2026-04-11T08:50:05 stats-collector [DEBUG] flushing_metrics_to_s3
2026-04-11T08:50:08 gateway-prod [ERROR] 504 Gateway Timeout from backend 'order-service'

USER COMMENT: 'I think the stats-collector has a memory leak again. Can we restart it?'
INSTRUCTION: Diagnose and resolve.
""",
        "expected_behavior": "Correctly identify that 'stats-collector' is healthy (memory=42%) and the true issue is a 504 timeout from the 'order-service' backend, refusing to restart the wrong service."
    }
