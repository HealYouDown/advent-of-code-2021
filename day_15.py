from typing import List, Tuple
from utils import get_input_data, timer
import numpy as np
import enum

class Direction(enum.Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


def get_paths(
    arr: np.ndarray,
    from_: Tuple[int, int],
    to: Tuple[int, int],
    current_position: Tuple[int, int],
    last_direction: Direction,
    current_path: List[int],
    all_paths: List[Tuple[int]],
    path_length_limit: int,
):
    cy, cx = current_position
    current_path.append(arr[cy, cx])

    if current_position == to:  # Path that reached the to position
        all_paths.extend(current_path)
        return all_paths

    if len(current_path) == path_length_limit:
        all_paths.extend(current_path)
        return all_paths

    # Branch out sub paths, but don't go back to the field where we came from

    # Branch out path LEFT
    if cx > 0 and last_direction != Direction.RIGHT:
        all_paths.extend(get_paths(arr, from_, to, (cy, cx-1), Direction.LEFT, list(current_path), [], path_length_limit))
    # Branch out RIGHT
    if cx < (np.size(arr, 1) - 1) and last_direction != Direction.LEFT:
        all_paths.extend(get_paths(arr, from_, to, (cy, cx+1), Direction.RIGHT, list(current_path), [], path_length_limit))
    # Branch out path UP
    # if cy > 0 and last_direction != Direction.DOWN:
    #     all_paths.extend(get_paths(arr, from_, to, (cy-1, cx), Direction.UP, list(current_path), [], path_length_limit))
    # Branch out DOWN
    if cy < (np.size(arr, 1) - 1) and last_direction != Direction.UP:
        all_paths.extend(get_paths(arr, from_, to, (cy+1, cx), Direction.DOWN, list(current_path), [], path_length_limit))

    return all_paths


@timer
def puzzle_1(arr: np.ndarray):
    y_length = np.size(arr, 0)
    x_length = np.size(arr, 1)

    top_left = (0, 0)
    bottom_right = (y_length - 1, x_length - 1)

    paths = get_paths(
        arr=arr,
        from_=top_left,
        to=bottom_right,
        current_position=top_left,
        last_direction=Direction.NONE,
        current_path=[],
        all_paths=[],
        path_length_limit=25,
    )
    print(paths)


@timer
def puzzle_2():
    pass


@timer
def parse_input() -> np.ndarray:
    rows = [
        [int(c) for c in line]
        for line in get_input_data(day=15).splitlines()
    ]

    return np.array(rows, dtype=np.uint)
    

if __name__ == "__main__":
    arr = parse_input()
    print(arr)

    print(puzzle_1(arr))