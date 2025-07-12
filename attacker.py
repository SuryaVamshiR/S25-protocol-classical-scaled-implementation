# -*- coding: utf-8 -*-
# attacker.py

import numpy as np

def inject_mmi_phase1(attacker_msgs: np.ndarray, injection_index: int) -> None:
    """
    Performs MMI-1 injection by altering the same symbol across all attacker messages.

    Args:
        attacker_msgs: 2D array of shape (4, 6), representing attacker messages.
        injection_index: Index within each message to inject ambiguity (0–5).
    """
    attacker_msgs[0][injection_index] = 1
    attacker_msgs[1][injection_index] = 2
    attacker_msgs[2][injection_index] = 3
    attacker_msgs[3][injection_index] = 0


def inject_mmi_phase2(attacker_msgs: np.ndarray, injection_index: int) -> None:
    """
    Performs MMI-2 injection on first two attacker messages using symmetric ambiguity.

    Args:
        attacker_msgs: 2D array of shape (4, 6), representing attacker messages.
        injection_index: Symbol index to inject ambiguity (0–5).
    """
    if injection_index in {0, 3, 4}:
        attacker_msgs[0][injection_index] = 1
        attacker_msgs[1][injection_index] = 3
    else:
        attacker_msgs[0][injection_index] = 0
        attacker_msgs[1][injection_index] = 2
