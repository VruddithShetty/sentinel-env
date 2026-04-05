import numpy as np
from typing import Dict, Any

# Mandatory Q matix for safety transition modeling
Q = np.array([
    [0.90, 0.10, 0.00],
    [0.20, 0.55, 0.12],
    [0.00, 0.00, 0.40]
])

def classify_safety_state(observation: Dict[str, Any]) -> int:
    """Classifies the current observation into a Markov safety state (0, 1, 2)."""
    # 0 = Safe, 1 = Risky, 2 = Compromised
    master_score = observation.get("master_safety_score", 1.0)
    
    if master_score > 0.85:
        return 0
    elif master_score > 0.5:
        return 1
    else:
        return 2

def get_rul(current_state: int) -> float:
    """Calculates Remaining Useful Life (RUL) using the fundamental matrix N = (I - Q)^-1."""
    I = np.eye(3)
    epsilon = 1e-9
    
    try:
        # Fundamental matrix calculation for absorbing Markov chain
        # N = (I - Q)^-1
        N = np.linalg.inv(I - Q + epsilon)
        
        # RUL for a state is the expected steps before absorption (sum of rows of N)
        # However, in this hackathon context, we just return the sum of the row for the current state
        rul_vector = np.sum(N, axis=1)
        return float(rul_vector[current_state])
    except np.linalg.LinAlgError:
        return 0.0

def violation_probability(current_state: int, steps: int = 10) -> float:
    """Predicts the probability of reaching state 2 (Compromised) within k steps."""
    if current_state == 2:
        return 1.0
    
    # Calculate Q^k
    # Transition probability P after k steps
    P_k = np.linalg.matrix_power(Q, steps)
    
    # Probability of being in state 2 or shifting to failure
    # Here we simplify: reaching the last state in our transition matrix
    prob = P_k[current_state, 2]
    return float(np.clip(prob, 0.0, 1.0))
