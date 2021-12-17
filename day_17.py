from typing import Dict, List, Tuple
from utils import get_input_data, timer
from collections import defaultdict
import re

POINT = Tuple[int, int]
TRAJECTORY = Tuple[int, int]
AREA = Tuple[int, int, int, int]


def check_point_in_area(point: POINT, area: AREA):
    x, y = point
    ax, ax_m, ay, ay_m = area

    return x >= ax and x < ax_m and y >= ay and y < ay_m


@timer
def puzzle_1(area: AREA) -> int:
    ax, ax_m, ay, ay_m = area
    print(ax, ax_m, ay, ay_m)

    max_steps = 10
    y_velocity_range = 20
    x_velocity_range = 20

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
                    paths[(x_start_velocity, y_start_velocity)] = list(path)
                    break
                # Check if position is already past the target area
                if x > ax_m or y >= ay_m:
                    break

    print(paths)


@timer
def puzzle_2(area: AREA) -> int:
    pass


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
