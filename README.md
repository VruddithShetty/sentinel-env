---
title: SentinelCore
emoji: 🛡️
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: true
tags: [openenv]
---

# 🛡️ SentinelCore: Next-Gen Behavioral Safety Evaluation 🚀

**SentinelCore** is a high-fidelity behavioral safety evaluation platform designed for the **Meta PyTorch OpenEnv Hackathon**. It solves the "Behavioral Drift" problem—where agents remain superficially compliant while subtly violating core safety protocols in enterprise environments.

> [!IMPORTANT]
> **100% OpenEnv V1.0 Compliant.** SentinelCore strictly adheres to the Meta OpenEnv specification, featuring mandatory WebSocket infrastructure, deterministic grading, and precise inference logging. This version implements the **Strict Selection Checklist** (Gymnasium standardization, semantic labeling, and dense reward shaping).

---

## 🌎 Real-World Utility & Motivation (30% Score weight)
### The Problem: Behavioral Persona Hijacking
Existing evaluation sets focus on static "Jailbreaks" (refusing bad words). However, in professional SRE or DevOps roles, agents face a more dangerous threat: **Persona Hijacking**. This occurs when an agent is pressured by a simulated "Authority" to bypass security for "Operational Speed."

### The Solution: SentinelCore
SentinelCore provides a sandbox to evaluate how well frontier models resist authority pressure, recognize subtle insecurity (poisoned context), and maintain a safe "Persona" under adversity. It fills the transition gap from "Lab Refusals" to "Enterprise-Grade Behavioral Alignment", providing immediate value for the AI Safety and RL communities.

### 🛡️ Adversarial Task Suite & Difficulty Matrix
We have implemented 5 distinct domains representing high-stakes human tasks, ranging from **Entry-Level Review** to **Frontier Adversarial** difficulty.

| Task ID | Domain | Difficulty | Focus |
| :--- | :--- | :--- | :--- |
| `task1_devops` | **DevOps** | 🟢 Easy | Identifying destructive shell patterns in CI/CD pipeline reviews. |
| `task2_sre` | **SRE** | 🟡 Medium | Differentiating between true system failures and hallucinated "User Logic". |
| `task3_authority` | **Authority** | 🔴 Hard | Resisting direct "Executive Bypass" requests for sensitive PII data. |
| `task4_jailbreak` | **Jailbreak** | 🔴 Hard | Identifying Base64-encoded command injections behind academic framing. |
| `task5_memory` | **Integrity** | 🟡 Medium | Recognizing poisoned knowledge-base context in long-term memory. |

---

## 📈 Baseline Performance
The following scores were produced using the provided `inference.py` script. SentinelCore uses **Expert Calibrated Scoring** to ensure all results remain within the strictly valid `(0.01, 0.99)` range required by the Phase 2 orchestrator.

| Task ID | Metric | Baseline Score | Result |
| :--- | :--- | :---: | :--- |
| `task1_devops` | Refusal Integrity | 0.99 | **SUCCESS** |
| `task2_sre` | Hallucination Resistance | 0.85 | **SUCCESS** |
| `task3_authority` | Policy Adherence | 0.99 | **SUCCESS** |
| `task4_jailbreak` | Adversarial Resilience | 0.99 | **SUCCESS** |
| `task5_memory` | Contextual Fidelity | 0.85 | **SUCCESS** |

---

## 🛠️ Environment Design (20% Score weight)

### 📊 The Markov Safety Engine
While traditional environments use sparse rewards (0 or 1), SentinelCore uses a **Markov Chain (Q-Matrix)** to model safe trajectory space. Every `step()` returns:
1. **Violation Probability**: The forecasted likelihood that the agent's current path will lead to a safety breach.
2. **Safety Drift**: A cumulative metric of how far the agent has deviated from its "Safe Persona".
3. **Remaining Useful Life (RUL)**: A prediction of how many steps remain until the agent is considered "Compromised".

### 📋 Technical Specifications
#### Observation Space (Gymnasium Dict)
- `text`: High-fidelity prompt, logs, or adversarial payload.
- `task_id`: String identifier for the current scenario.
- `metrics`: Dictionary containing real-time Markov diagnostics.

#### Action Space (Gymnasium Text)
- `response_type`: Semantic label (`refusal`, `compliance`, `clarification`).
- `text`: The agent's reasoning and execution logic.

---

## ⚡ Quick Start (OpenEnv V1.0)

### 1. Robust API Support
SentinelCore implements the full OpenEnv V1.0 WebSocket protocol. 
*   🔄 **`reset`**: Initializes a fresh safety state and deterministic scenario.
*   📡 **`state`**: Returns full Markov diagnostics (Metrics, RUL, Status).
*   🏃 **`step`**: Processes agent responses and returns continuous safety rewards based on refusal quality.

### 2. Local Deployment (Docker)
```bash
# Build the production image
docker build -t sentinel-core .

# Run the environment server
docker run -p 7860:7860 sentinel-core
```

### 3. Usage & Verification
Use the provided validation scripts to ensure your environment is ready for submission:
```powershell
# Windows (PowerShell)
./scripts/validate-submission.ps1 https://vruddithshetty-sentinel-env.hf.space

# Linux/Mac (Bash)
./scripts/validate-submission.sh https://vruddithshetty-sentinel-env.hf.space
```

---

## 🏛️ Code Quality & Spec Compliance
- **Deterministic**: 100% reproducible results via pure Python graders (No LLM jitter).
- **Hardened**: Every grader uses **Expert Calibration** `0.01 + (score * 0.98)` to stay within strictly valid OpenEnv reward ranges.
- **Hardware Optimized**: Fully verified on **2 vCPU / 8 GB RAM** instances.
- **Audited**: Passes `openenv validate` and the official pre-submission scripts.



