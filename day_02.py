from typing import List, Tuple
from utils import timer, get_input_data


@timer
def puzzle_1(data):
    x, y = 0, 0

    for cmd, value in data:
        if cmd == "forward":
            x += value
        elif cmd == "up":
            y -= value
        elif cmd == "down":
            y += value

    return x * y


@timer
def puzzle_2(data):
    x, y, aim = 0, 0, 0

    for cmd, value in data:
        if cmd == "forward":
            x += value
            y += aim * value
        elif cmd == "up":
            aim -= value
        elif cmd == "down":
            aim += value

    return x * y


@timer
def parse_input() -> List[Tuple[str, int]]:
    data = []
    for line in get_input_data(day=2).splitlines():
        s = line.split()
        data.append((s[0], int(s[1])))

    return data


if __name__ == "__main__":
    data = parse_input()

    print(puzzle_1(data))
    print(puzzle_2(data))
