from typing import Dict, List, Tuple
from utils import get_input_data, timer
from collections import defaultdict


POINT = Tuple[int, int]

class Line:
    def __init__(self, p1: POINT, p2: POINT) -> None:
        self._p1 = p1
        self._p2 = p2

    def __repr__(self) -> str:
        return f"<Line {self._p1} -> {self._p2}>"

    def get_points(
        self,
        diagonal_lines: bool,
    ) -> List[POINT]:
        """Returns a list with all points in between p1 and p2.

        Args:
            diagonal_lines (bool): Whether to calculate vertical positions as well.

        Returns:
            List[POINT]: List with all points between p1 and p2.
        """
        x1, y1 = self._p1
        x2, y2 = self._p2

        if x1 == x2:  # vertical line
            min_y, max_y = (y1, y2) if y1 < y2 else (y2, y1)
            return [(x1, y) for y in range(min_y, max_y+1)]

        elif y1 == y2:  # horizontal line
            min_x, max_x = (x1, x2) if x1 < x2 else (x2, x1)
            return [(x, y1) for x in range(min_x, max_x+1)]

        elif diagonal_lines:
            dy = 1 if y1 < y2 else -1
            dx = 1 if x1 < x2 else -1
            l = (y1 - y2 if y1 > y2 else y2 - y1) + 1  # length of the diagonal line

            return [(x1+(dx*i), y1+(dy*i)) for i in range(l)]

        return []  # Return for diagonal = True


@timer
def puzzle_1(lines: List[Line]) -> int:
    counter: Dict[POINT, int] = defaultdict(int)
    overlapping_points = 0

    for line in lines:
        for point in line.get_points(diagonal_lines=False):
            counter[point] += 1

    for point, count in counter.items():
        if count >= 2:
            overlapping_points += 1

    return overlapping_points


@timer
def puzzle_2(lines: List[Line]):
    counter: Dict[POINT, int] = defaultdict(int)
    overlapping_points = 0

    for line in lines:
        for point in line.get_points(diagonal_lines=True):
            counter[point] += 1

    for point, count in counter.items():
        if count >= 2:
            overlapping_points += 1

    return overlapping_points


@timer
def parse_input() -> List[Line]:
    lines = []

    for line in get_input_data(day=5).splitlines():
        p1, p2 = line.split(" -> ")

        lines.append(Line(
            p1=tuple(int(n) for n in p1.split(",")),
            p2=tuple(int(n) for n in p2.split(",")),
        ))

    return lines


if __name__ == "__main__":
    lines = parse_input()

    print(puzzle_1(lines))
    print(puzzle_2(lines))
