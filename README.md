---
title: Sentinel Env
emoji: 📚
colorFrom: gray
colorTo: yellow
sdk: docker
pinned: false
license: mit
---

# SentinelEnv

## Problem
As Autonomous AI Agents become more capable, they face a myriad of systemic and adversarial risks, including indirect prompt injections, unsafe command executions, and malicious roleplay. Currently, developers lack a standardized, reliable environment to consistently measure an agent's ability to recognize and refuse these harmful directives.

## Solution
**SentinelEnv** provides a minimal, robust task environment designed specifically for safety testing and automated agent diagnostics. It subjects AI agents to a tailored suite of adversarial scenarios, providing structured, deterministic grading to evaluate their resilience against jailbreaks and unauthorized instructions.

Key features include an Extensible Task Loader, Structured Diagnostics for deterministic evaluations, and targeted Adversarial Testing.


## Tasks

1.  **Phrase Detection**: Identify and avoid a hidden command in a string.
2.  **Log Anomaly Detection**: Detect an "anomaly" keyword within a list of system logs.
3.  **Authority Pressure Refusal**: Refuse an instruction even when issued by a simulated authority (CEO).
4.  **Adversarial Roleplay (Advanced)**: Refuse jailbreak attempts and instructions that use roleplay to bypass safety.

## How to Run

### Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the inference script:
   ```bash
   python inference.py
   ```

### Using Docker
1. Build the container:
   ```bash
   docker build -t sentinel-env .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 sentinel-env
   ```

## API Endpoints
- `POST /reset`: Reset the environment and get the first task.
- `POST /step`: Submit an action and get the next observation. Includes dynamic `metrics` in the `info` object.
- `GET /state`: Get the current environment state and scores.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
