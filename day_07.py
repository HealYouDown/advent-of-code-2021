from typing import Dict, List

from utils import get_input_data, timer
import sys


# That class is so useless
class CrabMarine:
    def __init__(self, pos: int) -> None:
        self._pos = pos

    @property
    def pos(self) -> int:
        return self._pos

    def calculate_fuel_cost(self, to: int) -> int:
        return abs(self._pos - to)


@timer
def puzzle_1(crabs: List[CrabMarine]) -> int:
    all_positions = [c.pos for c in crabs]
    min_ = min(all_positions)
    max_ = max(all_positions)

    d: Dict[int, List[int]] = {}
    for hp in range(min_, max_):
        d[hp] = [crab.calculate_fuel_cost(hp)
                 for crab in crabs]

    best_pos, best_fuel_cost = None, sys.maxsize
    for pos, fuel in d.items():
        if sum(fuel) < best_fuel_cost:
            best_fuel_cost = sum(fuel)
            best_pos = pos

    return f"Pos {best_pos} with {best_fuel_cost} fuel"


@timer
def puzzle_2(crabs: List[CrabMarine]):
    all_positions = [c.pos for c in crabs]
    min_ = min(all_positions)
    max_ = max(all_positions)

    exponential_fuel_map = {}
    for i in range(min_, max_+1):
        exponential_fuel_map[i] = sum(range(1, i+1))

    d: Dict[int, List[int]] = {}
    for hp in range(min_, max_):
        d[hp] = [exponential_fuel_map[crab.calculate_fuel_cost(hp)]
                 for crab in crabs]

    best_pos, best_fuel_cost = None, sys.maxsize
    for pos, fuel in d.items():
        if sum(fuel) < best_fuel_cost:
            best_fuel_cost = sum(fuel)
            best_pos = pos

    return f"Pos {best_pos} with {best_fuel_cost} fuel"


@timer
def parse_input() -> List[CrabMarine]:
    return [CrabMarine(int(i)) for i in get_input_data(day=7).split(",")]


if __name__ == "__main__":
    crabs = parse_input()

    print(puzzle_1(crabs))
    print(puzzle_2(crabs))
