# utils.py

import numpy as np
from typing import List, Tuple

def generate_file(size: int) -> np.ndarray:
    """
    Generates a random symbol stream of integers in [0, 3].

    Args:
        size: Length of the stream.

    Returns:
        A NumPy array of random integers between 0 and 3.
    """
    return np.random.randint(0, 4, size, dtype=np.int8)


def compute_symbol_distance(msg1: np.ndarray, msg2: np.ndarray, inf_val: int = 100000) -> int:
    """
    Computes custom symbolic distance between two messages.

    Rules:
    - If any symbol differs by 2 → return inf_val (invalid pair).
    - If difference is 1 or 3 → add 1 to total distance.
    - If difference is 0 → add 0 to total distance.

    Args:
        msg1: First message array.
        msg2: Second message array.
        inf_val: Value returned for invalid message pairs.

    Returns:
        Integer representing symbolic distance.
    """
    dist = 0
    for a, b in zip(msg1, msg2):
        diff = abs(a - b)
        if diff == 2:
            return inf_val
        elif diff in {1, 3}:
            dist += 1
        else:  # diff == 0
            dist += 0
    return dist


def count_pattern_instances(msg: np.ndarray, stream: np.ndarray) -> int:
    """
    Counts number of exact occurrences of a message pattern in the symbol stream.

    Args:
        msg: The message pattern to search for.
        stream: The symbol stream.

    Returns:
        Number of instances found.
    """
    count = 0
    for i in range(len(stream) - len(msg)):
        if np.all(stream[i:i + len(msg)] == msg):
            count += 1
    return count


def store_message_positions(msg: np.ndarray, stream: np.ndarray) -> List[int]:
    """
    Finds all positions where 'msg' occurs in 'stream' and returns end indices.

    Args:
        msg: Message to locate.
        stream: Symbol stream.

    Returns:
        List of end indices where message was found.
    """
    positions = []
    for i in range(len(stream) - len(msg)):
        if np.all(stream[i:i + len(msg)] == msg):
            positions.append(i+6)
    return positions


def reconstruct_state(stream: np.ndarray, positions: List[int], window: int = 6) -> np.ndarray:
    """
    Reconstructs state array from given positions in the symbol stream.

    Each state contains 'window' symbols followed by position marker.

    Args:
        stream: Symbol stream.
        positions: Start indices to extract state.
        window: Length of message window.

    Returns:
        A NumPy array of shape (len(positions), window + 1).
    """
    state = np.zeros((len(positions), window + 1), dtype=np.int32)
    for i, pos in enumerate(positions):
        if pos + window <= len(stream):
            state[i, :window] = stream[pos:pos + window]
            state[i, -1] = pos+window
    return state


def filter_state_by_message(msg: np.ndarray, state: np.ndarray, window: int = 6) -> List[int]:
    """
    Filters state entries that do not conflict with message symbols.

    A state entry is valid if no symbol differs from msg by 2.

    Args:
        msg: Reference message.
        state: State array with symbolic sequences.
        window: Symbol length in message.

    Returns:
        List of indices in state array that are valid.
    """
    indices = []
    for i, row in enumerate(state):
        if all(abs(msg[j] - row[j]) != 2 for j in range(window)):
            indices.append(i)
    return indices


def normalize_positions(positions: List[int], max_val: int) -> List[int]:
    """
    Cleans position list by removing zeroes and out-of-bound entries.

    Args:
        positions: Raw position values.
        max_val: Maximum allowed value (e.g. stream size - block length).

    Returns:
        Filtered position list.
    """
    return [p for p in positions if 0 < p <= max_val]


def sort_and_deduplicate(positions: List[int]) -> List[int]:
    """
    Returns sorted list of unique positions.

    Args:
        positions: List of position integers.

    Returns:
        Sorted and deduplicated list.
    """
    return sorted(list(set(positions)))


def select_random_subarray(arr: np.ndarray, size: int) -> np.ndarray:
    """
    Selects a random subarray of specified size from input array.

    Args:
        arr: Input array.
        size: Size of subarray to select.

    Returns:
        Random subarray of length 'size'.
    """
    indices = np.random.choice(len(arr), size, replace=False)
    return arr[indices]