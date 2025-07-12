# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 17:52:35 2025

@author: Surya Vamshi R
"""

# test_cascade_runs.py

import numpy as np
import matplotlib.pyplot as plt
from initial_setup import generate_initial_state
from cascade_round import run_cascade_round
from config import MAX_CYCLES

def run_single_trial() -> int:
    efile, msg, attacker_msgs, state, attacker_state, lrm = generate_initial_state()

    if state.shape[0] == 0:
        return 0

    # Choose random message from initial state
    index = np.random.randint(0, state.shape[0])
    msg = state[index, :6]

    for _ in range(MAX_CYCLES):
        msg, attacker_msgs, state, attacker_state = run_cascade_round(
            msg, attacker_msgs, state, attacker_state, lrm, efile
        )
        if state.shape[0] <= 1:
            break

    return _
def main():
    runs = 100
    results = []

    for i in range(runs):
        length = run_single_trial()
        results.append(length)
        print(f"Trial {i + 1}: Final attacker state length = {length}")

    # Plot histogram
    plt.figure(figsize=(8, 5))
    plt.hist(results, bins=20, color='darkred', edgecolor='white', alpha=0.8)
    plt.title("receiver space collapse")
    plt.xlabel("receiver round Length")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("Receiver_round_distribution.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()