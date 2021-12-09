from typing import Dict, List, Tuple, Union
import numpy as np
from utils import get_input_data, timer

Position = Tuple[int, int]  # x, y


def get_neighbors(arr: np.ndarray, x: int, y: int, rows: int, cols: int) -> List[Tuple[Position, int]]:
    neighbors = []

    if y != 0:  # top neighbor
        neighbors.append(((x, y-1), arr[y-1][x]))
    if y != (rows-1):  # bottom neighbor
        neighbors.append(((x, y+1), arr[y+1][x]))
    if x != 0:  # left side
        neighbors.append(((x-1, y), arr[y][x-1]))
    if x != (cols-1):
        neighbors.append(((x+1, y), arr[y][x+1]))

    return neighbors


def get_low_points(arr: np.ndarray) -> List[Tuple[Position, int]]:
    low_points = []
    rows = np.size(arr, 0)
    cols = np.size(arr, 1)

    for y in range(rows):
        for x in range(cols):
            value = arr[y][x]
            neighbors = get_neighbors(arr, x, y, rows, cols)

            if all(value < n for _, n in neighbors):
                low_points.append(((x, y), value))

    return low_points


def check_flow_to_low_point(
    arr: np.ndarray,
    x: int,
    y: int,
    rows: int,
    cols: int,
    low_points: List[Tuple[Position, int]],
) -> Position:
    value = arr[y][x]
    neighbors = get_neighbors(arr, x, y, rows, cols)

    for neighbor in neighbors:
        n_pos, n = neighbor

        if neighbor in low_points:
            # Found one that flows into a low point
            return n_pos

        # Check if any neighbor is value is lower, so a chain that
        # could potentially flow into a low point
        if n < value:
            x, y = n_pos
            return check_flow_to_low_point(arr, x, y, rows, cols, low_points)


@timer
def puzzle_1(arr: np.ndarray) -> int:
    low_points = get_low_points(arr)
    return sum([l+1 for _, l in low_points])


@timer
def puzzle_2(arr: np.ndarray):
    low_points = get_low_points(arr)
    basin_size_counter: Dict[Position, int] = {}

    # each low points counts as +1 for the basin
    for lp_pos, _ in low_points:
        basin_size_counter[lp_pos] = 1


    rows = np.size(arr, 0)
    cols = np.size(arr, 1)
    for y in range(rows):
        for x in range(cols):
            value = arr[y][x]
            lp_that_x_y_flows_to = None

            if value != 9 and (x, y) not in basin_size_counter:
                lp_that_x_y_flows_to = check_flow_to_low_point(arr, x, y, rows, cols, low_points)
                basin_size_counter[lp_that_x_y_flows_to] += 1

    # Get the three largest basins and multiply them
    a, b, c, *_ = sorted(basin_size_counter.values(), reverse=True)
    return a * b * c


@timer
def parse_input() -> np.ndarray:
    r = []
    for line in get_input_data(day=9).splitlines():
        r.append([int(i) for i in line])

    return np.array(r, dtype=np.uint8)


if __name__ == "__main__":
    arr = parse_input()

    print(puzzle_1(arr))
    print(puzzle_2(arr))
