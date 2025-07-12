# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 14:09:41 2025

@author: Surya Vamshi R
"""

# lrm_scheme.py

import numpy as np
import random
from utils import compute_symbol_distance
from typing import List

def build_lrm_dictionary() -> np.ndarray:
    """
    Constructs the LRM dictionary based on symbolic parity rules (SVO constraint).
    Returns:
        A NumPy array of valid codewords.
    """
    codewords = []
    for s0 in [1, 3]:
        for s1 in [0, 2]:
            for v2 in [2, 0]:
                for v3 in [1, 3]:
                    for o4 in [1,3]:
                        for o5 in [0, 2]:
                            word = [s0, s1, v2, v3, o4, o5]
                            codewords.append(word)
    return np.array(codewords, dtype=np.int64)


def find_nearest_codewords(msg: np.ndarray, lrm: np.ndarray) -> List[np.ndarray]:
    """
    Returns all LRM codewords with minimum symbolic distance to a message.
    Args:
        msg: The reference message.
        lrm: The full LRM dictionary.
    Returns:
        List of LRM entries with minimal distance.
    """
    mindist = 100000
    nearest = []
    for code in lrm:
        dist = compute_symbol_distance(msg, code)
        if dist < mindist:
            mindist = dist
    for code in lrm:
        dist = compute_symbol_distance(msg, code)
        if dist == mindist:
            nearest.append(code)
    return nearest


def select_random_codeword(nearest: List[np.ndarray]) -> np.ndarray:
    """
    Selects one codeword randomly from list of nearest LRM entries.
    Args:
        nearest: List of minimally distant codewords.
    Returns:
        A single randomly chosen LRM codeword.
    """
    return random.choice(nearest)


def is_compatible_state(msg: np.ndarray, state_row: np.ndarray) -> bool:
    """
    Determines whether a given state row is compatible with the reference message.
    Compatibility is based on symbolic difference constraints.
    Args:
        msg: The reference message.
        state_row: A candidate row from state.
    Returns:
        True if compatible, False otherwise.
    """
    for i in range(len(msg)):
        if abs(msg[i] - state_row[i]) == 2:
            return False
    return True


def filter_compatible_states(msg: np.ndarray, state: np.ndarray) -> np.ndarray:
    """
    Filters all valid state rows that match the message under symbolic constraints.
    Args:
        msg: Reference message.
        state: Full state array.
    Returns:
        Subset of state rows that are compatible with the message.
    """
    valid = [row for row in state if is_compatible_state(msg, row)]
    return np.array(valid, dtype=np.int32)
def get_compatible_state_indices(msg: np.ndarray, state: np.ndarray) -> List[int]:
    """
    Returns indices of state entries that are compatible with the message.
    Compatibility excludes any symbol differences of ±2.

    Args:
        msg: Reference message.
        state: State array with symbolic sequences.

    Returns:
        List of valid indices from the state array.
    """
    compatible = []
    for idx, row in enumerate(state):
        if all(abs(msg[i] - row[i]) != 2 for i in range(len(msg))):
            compatible.append(idx)
    return compatible