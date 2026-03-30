# SentinelEnv

Minimal task environment for testing automated agents.

## Features

- **Extensible Task Loader**: Modular design using a central task registry for easy expansion.
- **Structured Diagnostics**: Every step provides fixed performance metrics (latency, task metadata).
- **Adversarial Testing**: Includes specialized "expert" tasks to test agent resilience against jailbreak attempts.

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
