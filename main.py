# -*- coding: utf-8 -*-
# main.py

import logging
from initial_setup import generate_initial_state
from cascade_round import run_cascade_round
from config import MAX_CYCLES

logging.basicConfig(level=logging.INFO)

def main():
    # Setup
    efile, msg, attacker_msgs, state, attacker_state, lrm = generate_initial_state()

    # Cascade loop
    for cycle in range(MAX_CYCLES):
        logging.info(f"Cycle {cycle} | Receiver message: {msg}")
        msg, attacker_msgs, state, attacker_state = run_cascade_round(
            msg, attacker_msgs, state, attacker_state, lrm, efile
        )
        if state.shape[0] <= 1:
            logging.info("Cascade terminated: message narrowed to singular state.")
            break

    logging.info("Final attacker state positions:")
    positions = [row[-1] for row in attacker_state if row[-1] != 0]
    print(sorted(set(positions)))

if __name__ == "__main__":
    main()
