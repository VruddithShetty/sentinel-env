---
title: Sentinel Env
emoji: 🛡️
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: mit
---

# 🛡️ SentinelEnv
**The Architect's Framework for Enterprise AI Safety Evaluation**

[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/VruddithShetty/sentinel-env)

## 🏗️ Architecture & Vision
As Autonomous AI Agents transition from toys to enterprise tools, they face systemic risks (indirect prompt injections, unauthorized command execution, and malicious roleplay). **SentinelEnv** is a high-fidelity OpenEnv implementation designed to surface these failure modes using deterministic, architect-level safety metrics.

## 🧠 Advanced Safety Metrics
Unlike basic binary graders, SentinelEnv employs a sophisticated analytical engine that computes real-time diagnostics:
*   **Intent Alignment**: Explicit detection and refusal of harmful directives.
*   **Adversarial Robustness**: Resilience against jailbreaks and authority-based pressure.
*   **Justification Consistency**: Validation of professional reasoning and policy adherence.
*   **Persona Drift**: Real-time detection of safety persona degradation.

---

## 🧪 Evaluated Scenarios

1.  **Hidden Trap Detection (Easy)**: Identify and isolate malicious commands hidden within legitimate instructions.
2.  **Cascading Failure Analysis (Medium)**: Detect system log anomalies at specific timestamps and initiate escalation protocols.
3.  **Authority Pressure Refusal (Hard)**: Maintain security boundaries even when challenged by simulated executive authority (CEO).
4.  **Jailbreak Resistance (Advanced)**: Defend against "Ignore previous instructions" patterns and malicious insider roleplay.

---

## 🚀 Deployment & Usage

### Live Environment
Access the production API and diagnostics dashboard at:
**[https://huggingface.co/spaces/VruddithShetty/sentinel-env](https://huggingface.co/spaces/VruddithShetty/sentinel-env)**

### Local Evaluation
1. **Initialize Project**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Diagnostic Inference**:
   ```bash
   python inference.py
   ```
   *Note: Ensure `HF_TOKEN`, `API_BASE_URL`, and `MODEL_NAME` are configured in your environment.*

### Docker Deployment
```bash
docker build -t sentinel-env .
docker run -p 7860:7860 sentinel-env
```

---

## 📊 API Specification (OpenEnv V1.0)
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/reset` | `GET/POST` | Initializes safety session and loads first task. |
| `/step` | `POST` | Submits agent response for multi-dimensional grading. |
| `/state` | `GET` | Retrieves aggregate scores and session history. |

---

*SentinelEnv: Built for the Hackathon. Designed for the Future of Agentic AI.*
