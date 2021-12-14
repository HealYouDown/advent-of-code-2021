from typing import Tuple, Dict, List
from utils import get_input_data, timer
from collections import Counter


def polymer_step(polymer_template: str, mapping: Dict[str, str], step: int) -> int:
    polymer: List[str] = list(polymer_template)

    for _ in range(step):
        polymer_tmp = []

        for index, char in enumerate(polymer):            
            try:
                next_char = polymer[index+1]
            except IndexError:
                polymer_tmp.append(char)
                break

            pair = char + next_char

            if pair in mapping:
                polymer_tmp.extend(char + mapping[pair])
            else:
                polymer_tmp.append(char)

        polymer = polymer_tmp

    counter = Counter(polymer)
    most_common = counter.most_common()
    mc = most_common[0][1]
    lc = most_common[-1][1]

    return mc - lc


@timer
def puzzle_1(polymer_template: str, mapping: Dict[str, str]):
    return polymer_step(polymer_template, mapping, 10)


@timer
def puzzle_2(polymer_template: str, mapping: Dict[str, str]):
    return polymer_step(polymer_template, mapping, 40)



@timer
def parse_input() -> Tuple[str, Dict[str, str]]:
    lines = get_input_data(day=14).splitlines()
    polymer_template = lines[0]

    mapping = {}
    for line in lines[2:]:
        a, b = line.split(" -> ")
        mapping[a] = b

    return polymer_template, mapping


if __name__ == "__main__":
    polymer_template, mapping = parse_input()

    print(puzzle_1(polymer_template, mapping))
    print(puzzle_2(polymer_template, mapping))
