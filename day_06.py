from typing import List

import numpy as np

from utils import get_input_data, timer


def calculate_children_after_n_days(num: int, days: int) -> int:
    arr = np.array([num], dtype=np.uint8)

    for _ in range(days):
        # Still to slow at 200+ days
        count = np.count_nonzero(arr == 0)  # Count 0 that will spawn new fish
        arr = np.where(arr == 0, arr + 6, arr - 1)  # Set zeros to 6 and everything else -1
        arr = np.concatenate([arr, np.full(count, 8, dtype=np.uint8)])  # add new 8 fish 

    return arr.size


@timer
def puzzle_1(data: List[int]) -> int:
    mapper = {
        initial_state: calculate_children_after_n_days(initial_state, 80)
        for initial_state in range(0, 9)
    }

    return sum([mapper[i] for i in data])

@timer
def puzzle_2(data: List[int]):
    mapper = {
        initial_state: calculate_children_after_n_days(initial_state, 256)
        for initial_state in range(0, 9)
    }

    return sum([mapper[i] for i in data])


@timer
def parse_input() -> List[int]:
    return [int(i) for i in get_input_data(day=6).split(",")]


if __name__ == "__main__":
    data = parse_input()

    print(puzzle_1(data))
    # print(puzzle_2(data))
