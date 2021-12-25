from utils import get_input_data, timer
import numpy as np


@timer
def puzzle_1(arr: np.ndarray) -> int:
    # I did not spend any time optimizing this at all,
    # it just loops through the whole field all the time xd

    step = 0
    step1_changed = True
    step2_changed = True
    while (step1_changed or step2_changed):
        step += 1
        shadow_arr = arr.copy()

        # east herd
        for y in range(np.size(arr, 0)):
            for x in range(np.size(arr, 1)):
                val = arr[y, x]
                if val == ">":  # Check right
                    try:
                        neighbor_val = arr[y, x+1]
                        across_bound = False
                    except IndexError:
                        neighbor_val = arr[y, 0]
                        across_bound = True

                    if neighbor_val == ".":  # free space to move to
                        shadow_arr[y, x] = "."  # update the current position to be empty
                        # update the new position
                        if across_bound:
                            shadow_arr[y, 0] = ">"
                        else:
                            shadow_arr[y, x+1] = ">"

        if np.array_equal(arr, shadow_arr):
            step1_changed = False
        else:
            step1_changed = True

        arr = shadow_arr
        shadow_arr = arr.copy()

        # south herd
        for y in range(np.size(arr, 0)):
            for x in range(np.size(arr, 1)):
                val = arr[y, x]
                if val == "v":  # check down
                    try:
                        neighbor_val = arr[y+1, x]
                        across_bound = False
                    except IndexError:
                        neighbor_val = arr[0, x]
                        across_bound = True

                    if neighbor_val == ".":  # free space to move to
                        shadow_arr[y, x] = "."  # update the current position to be empty
                        # update the new position
                        if across_bound:
                            shadow_arr[0, x] = "v"
                        else:
                            shadow_arr[y+1, x] = "v"

        if np.array_equal(arr, shadow_arr):
            step2_changed = False
        else:
            step2_changed = True

        arr = shadow_arr

    return step


@timer
def parse_input() -> np.ndarray:
    rows = [list(line) for line in get_input_data(day=25).splitlines()]
    return np.array(rows)


if __name__ == "__main__":
    arr = parse_input()

    print(puzzle_1(arr))
