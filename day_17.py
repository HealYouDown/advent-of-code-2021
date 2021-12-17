from typing import Dict, List, Tuple
from utils import get_input_data, timer
import sys
import re

POINT = Tuple[int, int]
TRAJECTORY = Tuple[int, int]
AREA = Tuple[int, int, int, int]


def get_paths(
    area: AREA,
    max_steps: int,
    y_velocity_range: int,
    x_velocity_range: int
) -> Dict[TRAJECTORY, List[POINT]]:
    ax, ax_m, ay, ay_m = area

    paths: Dict[TRAJECTORY, List[POINT]] = {}
    
    # x velocity can only be positive
    # y velocity can be negative (down) positive (up)
    for x_start_velocity in range(1, x_velocity_range):
        for y_start_velocity in range(-y_velocity_range, y_velocity_range):
            x, y = 0, 0
            x_velocity = x_start_velocity
            y_velocity = y_start_velocity
            path = []
            path.append((x, y))

            for _ in range(max_steps):
                x += x_velocity
                y += y_velocity

                if x_velocity != 0:
                    x_velocity = (x_velocity - 1) if x_velocity > 0 else (x_velocity + 1)
                y_velocity -= 1
                path.append((x, y))

                # Check if in bounds
                if (ax <= x <= ax_m) and (ay <= y <= ay_m):
                    paths[(x_start_velocity, y_start_velocity)] = path
                    break

                # Check if target is already missed
                if x > ax_m and y > ay_m:
                    break

    return paths


@timer
def puzzle_1(area: AREA) -> int:
    # Numbers found by just trying out different ones lol
    paths = get_paths(area, 550, 300, 100)

    highest_y = -sys.maxsize
    for points in paths.values():
        for point in points:
            if point[1] > highest_y:
                highest_y = point[1]   

    return highest_y


@timer
def puzzle_2(area: AREA) -> int:
    return len(get_paths(area, 550, 300, 100))



@timer
def parse_input() -> AREA:
    return [
        int(i)
        for i in re.findall(r"(\+|\-?\d{1,3})",
                            get_input_data(day=17))
    ]


if __name__ == "__main__":
    area = parse_input()

    print(puzzle_1(area))
    print(puzzle_2(area))
