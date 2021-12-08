from typing import List, Tuple

from utils import get_input_data, timer

NUMBER_TO_SEGMENTS = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}
UNIQUE_SEGMENT_NUMBERS = [1, 4, 7, 8]


@timer
def puzzle_1(data: List[Tuple[List[str], List[str]]]) -> int:
    unique_segments = [NUMBER_TO_SEGMENTS[n] for n in UNIQUE_SEGMENT_NUMBERS]

    counter = 0
    for _, output_values in data:
        for item in output_values:
            if len(item) in unique_segments:
                counter += 1

    return counter


@timer
def puzzle_2(data: List[Tuple[List[str], List[str]]]):
    pass


@timer
def parse_input() -> List[Tuple[List[str], List[str]]]:
    data = []
    for line in get_input_data(day=8).splitlines():
        p1, p2 = line.split(" | ")

        data.append(([p for p in p1.split(" ")], [p for p in p2.split(" ")]))

    return data


if __name__ == "__main__":
    data = parse_input()

    print(puzzle_1(data))
    print(puzzle_2(data))
