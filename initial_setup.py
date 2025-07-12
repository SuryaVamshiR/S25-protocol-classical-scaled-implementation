# -*- coding: utf-8 -*-
# initial_setup.py

import numpy as np
import random
from typing import Tuple
from utils import generate_file, count_pattern_instances, store_message_positions, reconstruct_state
from attacker import inject_mmi_phase1
from lrm_scheme import build_lrm_dictionary

def generate_initial_state(file_size: int = 100000) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generates initial file stream, messages, positions, and states for cascade start.

    Returns:
        - efile: Symbol stream
        - current_msg: Initial receiver message
        - attacker_msgs: Attacker variants (4x6)
        - state: Receiver state array
        - attacker_state: Attacker's state array
        - lrm: LRM dictionary
    """
    # Step 1: Create symbol stream
    efile = generate_file(file_size)

    # Step 2: Select random message from stream
    select_index = random.randint(0, file_size - 6)
    current_msg = efile[select_index:select_index + 6]

    # Step 3: Duplicate to attackers and inject MMI-1
    attacker_msgs = np.tile(current_msg, (4, 1))
    injection_idx = random.randint(0, 5)
    inject_mmi_phase1(attacker_msgs, injection_idx)

    # Step 4: Find message instances and positions
    receiver_positions = store_message_positions(current_msg, efile)
    attacker_positions = []
    for attacker in attacker_msgs:
        attacker_positions.extend(store_message_positions(attacker, efile))

    # Step 5: Reconstruct receiver and attacker states
    state = reconstruct_state(efile, receiver_positions)
    attacker_state = reconstruct_state(efile, attacker_positions)

    # Step 6: Generate LRM dictionary
    lrm = build_lrm_dictionary()

    return efile, current_msg, attacker_msgs, state, attacker_state, lrm
