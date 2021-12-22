import itertools
import re
from dataclasses import dataclass
from typing import List, Tuple

from utils import get_input_data, timer


@dataclass
class RebootStep:
    method: str
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int

    @classmethod
    def from_line(cls, line: str) -> "RebootStep":
        method = "on" if line.startswith("on") else "off"
        return cls(method, *[int(n) for n in re.findall(r"(\+|\-?\d+)", line)])

    def calculate_points_between(self) -> List[Tuple[int, int, int]]:
        """ Primitive try :D
        points = set()

        for x in range(self.x1, self.x2+1):
            for y in range(self.y1, self.y2+1):
                for z in range(self.z1, self.z2+1):
                    points.add((x, y, z))

        return points
        """
        
        # Still too "slow", so for P2, you probably need a mathematical solution
        # which I have no clue about
        return itertools.product(range(self.x1, self.x2+1),
                                 range(self.y1, self.y2+1),
                                 range(self.z1, self.z2+1))

    def position_in_range(self, x: Tuple[int, int], y: Tuple[int, int], z: Tuple[int, int]) -> bool:
        x_in_range = self.x1 >= x[0] and self.x2 <= x[1]
        y_in_range = self.y1 >= y[0] and self.y2 <= y[1]
        z_in_range = self.z1 >= z[0] and self.z2 <= z[1]

        return x_in_range and y_in_range and z_in_range


@timer
def puzzle_1(reboot_steps: List[RebootStep]) -> int:
    cubes = set()

    for step in reboot_steps:
        if step.position_in_range((-50, 50), (-50, 50), (-50, 50)):
            points = step.calculate_points_between()
            if step.method == "on":
                cubes.update(points)
            else:
                cubes.difference_update(points)

    return len(cubes)


@timer
def puzzle_2(reboot_steps: List[RebootStep]) -> int:
    cubes = set()

    for step in reboot_steps:
        points = step.calculate_points_between()
        if step.method == "on":
            cubes.update(points)
        else:
            cubes.difference_update(points)

    return len(cubes)


@timer
def parse_input() -> List[RebootStep]:
    return [
        RebootStep.from_line(line)
        for line in get_input_data(day=22).splitlines()
    ]


if __name__ == "__main__":
    reboot_steps = parse_input()

    print(puzzle_1(reboot_steps))
    # print(puzzle_2(reboot_steps))
