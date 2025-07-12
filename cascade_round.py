# -*- coding: utf-8 -*-
# cascade_round.py

import numpy as np
import random
from typing import Tuple
from utils import reconstruct_state
from lrm_scheme import find_nearest_codewords, select_random_codeword, get_compatible_state_indices
from attacker import inject_mmi_phase2

def run_cascade_round(
    current_msg: np.ndarray,
    attacker_msgs: np.ndarray,
    state: np.ndarray,
    attacker_state: np.ndarray,
    lrm: np.ndarray,
    efile: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Runs a single round of symbolic cascade including attacker injection and state evolution.

    Args:
        current_msg: Message propagated to receiver.
        attacker_msgs: Attacker message matrix (shape: 4x6).
        state: Receiver state array (symbol segments + position).
        attacker_state: Attacker’s corresponding state.
        lrm: LRM dictionary for symbolic codewords.
        efile: The full symbol stream.

    Returns:
        Tuple of:
            - Next message (np.ndarray)
            - Updated attacker messages (np.ndarray)
            - New receiver state (np.ndarray)
            - New attacker state (np.ndarray)
    """
    # After initial state reconstruction
    msg_index = random.randint(0, state.shape[0] - 1)
    current_msg = state[msg_index, :6]  # Extract only the symbol sequence, exclude position

    # Step 1: Select nearest LRM codewords
    nearest_codewords = find_nearest_codewords(current_msg, lrm)
    selected_codeword = select_random_codeword(nearest_codewords)

    # Step 2: Generate next message
    next_msg = np.copy(selected_codeword)

    # Step 3: Update attacker messages and inject MMI-2
    for i in range(4):
        attacker_msgs[i] = np.copy(next_msg)
    injection_idx = random.randint(0, 5)
    inject_mmi_phase2(attacker_msgs, injection_idx)

    # Step 4: Filter compatible states
    valid_indices_receiver = get_compatible_state_indices(next_msg, state)
    valid_positions_receiver = [state[i][-1] for i in valid_indices_receiver]
    new_state = reconstruct_state(efile, valid_positions_receiver)

    valid_indices_attacker = get_compatible_state_indices(attacker_msgs[0], attacker_state)
    valid_indices_attacker.extend(get_compatible_state_indices(attacker_msgs[1], attacker_state))
    valid_positions_attacker = [attacker_state[i][-1] for i in valid_indices_attacker]
    new_attacker_state = reconstruct_state(efile, valid_positions_attacker)

    return next_msg, attacker_msgs, new_state, new_attacker_state
