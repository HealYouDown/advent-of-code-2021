from typing import List, Tuple
from utils import get_input_data, timer
import numpy as np


def fold_array(arr: np.ndarray, instruction: str) -> np.ndarray:
    ins_splitted = instruction.split("=")
    fold_axis = ins_splitted[0]
    fold_at = int(ins_splitted[1])

    rows = np.size(arr, 0)
    cols = np.size(arr, 1)

    if fold_axis == "y":
        array_that_is_folded_in = arr[0:fold_at, 0:cols]
        array_to_fold = np.flip(arr[fold_at+1:rows, 0:cols], 0)
        new_arr = array_that_is_folded_in + array_to_fold
    elif fold_axis == "x":
        array_that_is_folded_in = arr[0:rows, 0:fold_at]
        array_to_fold = np.flip(arr[0:rows, fold_at+1:cols], 1)
        new_arr = array_that_is_folded_in + array_to_fold

    new_arr[new_arr >= 2] = 1
    return new_arr

@timer
def puzzle_1(arr: np.ndarray, instructions: List[str]) -> int:
    arr = fold_array(arr, instructions[0])
    return np.count_nonzero(arr == 1)

@timer
def puzzle_2(arr: np.ndarray, instructions: List[str]):
    for inst in instructions:
        arr = fold_array(arr, inst)

    s = ""
    with open("t.out", "w") as fp:
        for row in arr:
            s += "".join(["*" if r == 1 else " " for r in row])
            s += "\n"

    return s


@timer
def parse_input() -> Tuple[np.ndarray, List[str]]:
    instructions = []

    points_x = []
    points_y = []

    for line in get_input_data(day=13).splitlines():
        if line.startswith("fold along"):
            instructions.append(line.split(" ")[-1])
        else:
            if not line:  # empty line
                continue
            x, y = [int(i) for i in line.split(",")]
            points_x.append(x)
            points_y.append(y)

    points = zip(points_x, points_y)
    max_x = max(points_x)
    max_y = max(points_y)

    arr = np.zeros((max_y+1, max_x+1), dtype=np.uint8)
    for x, y in points:
        arr[y, x] = 1

    return arr, instructions


if __name__ == "__main__":
    arr, instructions = parse_input()

    print(puzzle_1(arr, instructions))
    print(puzzle_2(arr, instructions))
