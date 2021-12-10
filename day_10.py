import re
from typing import List
from utils import get_input_data, timer

PATTERN = re.compile(r"(\[\]|\(\)|\{\}|\<\>)")

OPENING_CHARS = ["(", "[", "<", "{"]
CLOSING_CHARS = [")", "]", ">", "}"]
SYNTAX_ERROR_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
} 
AUTOCOMPLETE_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


@timer
def puzzle_1(lines: List[str]) -> int:
    corrupted_chars = []

    for line in lines:
        while True:
            previous_line = line
            line = re.sub(PATTERN, "", line)
            if line == previous_line:
                break

        # The remaining line now consists of all unmatched pairs
        # e.g. {([(<{}[<>[]}>{[]{[(<()> -> {([(<[}>{{[(
        # the first closing character is the corrupted one
        for char in line:
            if char in CLOSING_CHARS:
                corrupted_chars.append(char)
                break

    return sum([SYNTAX_ERROR_SCORE[c] for c in corrupted_chars])


@timer
def puzzle_2(lines: List[str]):
    incomplete_lines = []

    # Taking the code from part 1 to filter out broken lines
    for line in lines:
        while True:
            previous_line = line
            line = re.sub(PATTERN, "", line)
            if line == previous_line:
                break

        if not any(c in CLOSING_CHARS for c in line):
            incomplete_lines.append(line)

    scores = []
    for line in incomplete_lines:
        # Chars to complete the line
        # [({([[{{ -> }}]])})]
        # (that replace chain is ugly, but the easiest solution here lol)
        completion_string = line[::-1].replace("(", ")").replace("[", "]").replace("{", "}").replace("<", ">")

        score = 0
        for char in completion_string:
            score *= 5
            score += AUTOCOMPLETE_SCORE[char]

        scores.append(score)

    return sorted(scores)[len(scores)//2]


@timer
def parse_input() -> List[str]:
    return get_input_data(day=10).splitlines()


if __name__ == "__main__":
    lines = parse_input()

    print(puzzle_1(lines))
    print(puzzle_2(lines))
