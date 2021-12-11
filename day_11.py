from utils import get_input_data, timer
import numpy as np


@timer
def puzzle_1(arr: np.ndarray) -> int:
    rows = np.size(arr, 0)
    cols = np.size(arr, 1)

    total_flash_count = 0

    for _ in range(100):
        arr += 1
        flashing_indicies = []

        while True:
            # Find all octopuses with >= 9
            res = np.where(arr > 9)
            # Create a list of indicies [(x, y), ...]
            indicies = list(zip(*res))
            # Filter out indicies that are already flashing
            indicies = [i for i in indicies if i not in flashing_indicies]
            # If no more indicies are left, we can stop the loop
            if not indicies:
                break
            # Keep track of the indicies that are flashing
            flashing_indicies.extend(indicies)
            # Update all neighbor indicies +1
            for x, y in indicies:
                x_min = x - 1 if x > 0 else 0
                x_max = x + 1 if x < (rows - 1) else x
                y_min = y - 1 if y > 0 else 0
                y_max = y + 1 if y < (cols - 1) else y

                arr[x_min:x_max+1, y_min:y_max+1] += 1  # type: ignore

        # Reset all octopuses with >= 9 to 0
        arr[arr > 9] = 0
        # Update the total flashing count 
        total_flash_count += len(flashing_indicies)

    return total_flash_count


@timer
def puzzle_2(arr: np.ndarray):
    rows = np.size(arr, 0)
    cols = np.size(arr, 1)

    step = 0
    while True:
        step += 1
        arr += 1
        flashing_indicies = []
        flash_count = 0

        while True:
            # Find all octopuses with >= 9
            res = np.where(arr > 9)
            # Create a list of indicies [(x, y), ...]
            indicies = list(zip(*res))
            # Filter out indicies that are already flashing
            indicies = [i for i in indicies if i not in flashing_indicies]
            # If no more indicies are left, we can stop the loop
            if not indicies:
                break
            # Keep track of the indicies that are flashing
            flashing_indicies.extend(indicies)
            # Update all neighbor indicies +1
            for x, y in indicies:
                x_min = x - 1 if x > 0 else 0
                x_max = x + 1 if x < (rows - 1) else x
                y_min = y - 1 if y > 0 else 0
                y_max = y + 1 if y < (cols - 1) else y

                arr[x_min:x_max+1, y_min:y_max+1] += 1  # type: ignore

        # Reset all octopuses with >= 9 to 0
        arr[arr > 9] = 0
        # Update the total flashing count 
        flash_count = len(flashing_indicies)

        if flash_count == len(arr.flatten()):
            return step


@timer
def parse_input() -> np.ndarray:
    rows = [[int(i) for i in line]
            for line in get_input_data(day=11).splitlines()]
    return np.array(rows, dtype=np.uint8)


if __name__ == "__main__":
    arr = parse_input()
    print(puzzle_1(arr.copy()))
    print(puzzle_2(arr.copy()))
