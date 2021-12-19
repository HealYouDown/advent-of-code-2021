from functools import reduce
import math
import re
from collections import defaultdict, deque
from itertools import permutations
from typing import DefaultDict, Dict, List, Union

from utils import get_input_data, timer

SNAILFISH_NUMBER = List[Union["SNAILFISH_NUMBER", int]]

class NO_MORE_EXPLOSION_EXCEPTION(Exception):
    pass


class NO_MORE_SPLIT_EXCEPTION(Exception):
    pass


def find_depths(
    sn: SNAILFISH_NUMBER,
    depth: int,
    storage: DefaultDict[int, list],
):
    storage[depth].append(sn)

    for left, right in zip(*[iter(sn)]*2):
        if isinstance(left, list):
            find_depths(left, depth+1, storage)

        if isinstance(right, list):
            find_depths(right, depth+1, storage)

    return storage


def list_to_string(l: List[int]) -> str:
    # Pads every single-digit number with a space to prevent a number
    # that changes its value from 9 to 10 to shift all indicies
    s = str(l).replace(" ", "")
    return s  # return re.sub(r"(\b\d\b)", r" \1", s)


def explode_snailfish_number(sn: SNAILFISH_NUMBER) -> SNAILFISH_NUMBER:
    sn_string = list_to_string(sn)

    depths = find_depths(sn, 0, defaultdict(list))
    try:
        first_exploding = depths[4][0]
    except IndexError:
        raise NO_MORE_EXPLOSION_EXCEPTION

    # Find first exploding in the string
    pattern = f"({re.escape(list_to_string(first_exploding))})"
    exploding_matches = list(re.finditer(pattern, sn_string))

    # Check all exploding matches for [ in front of them - they should have at least 4
    filtered_exploding_matches = []
    for match in exploding_matches:
        substring = sn_string[:match.span()[0]]
        count_open = substring.count("[")
        count_closed = substring.count("]")
        nested_depth = count_open - count_closed

        if nested_depth == 4:
            filtered_exploding_matches.append(match)

    exploding_match: re.Match = filtered_exploding_matches[0]
    exploding_pair_left_value, exploding_pair_right_value = eval(exploding_match.group(0))

    # Find the first regular number on the left and right side
    num_pattern = r"\d{1,3}"
    left_matches = list(re.finditer(num_pattern, sn_string[:exploding_match.span()[0]]))
    right_matches = list(re.finditer(num_pattern, sn_string[exploding_match.span()[1]:]))

    if left_matches:
        left_match: re.Match = left_matches[-1]

        left_num = int(left_match.group(0))
        left_part_1 = sn_string[:left_match.span()[0]]
        left_part_2 = sn_string[left_match.span()[1]:exploding_match.span()[0]]

        left_part = f"{left_part_1}{left_num + exploding_pair_left_value}{left_part_2}"
    else:
        left_part = sn_string[:exploding_match.span()[0]]

    if right_matches:
        right_match: re.Match = right_matches[0]

        right_num = int(right_match.group(0))
        right_part_1 = sn_string[exploding_match.span()[1]:(exploding_match.span()[1] + right_match.span()[0])]
        right_part_2 = sn_string[(exploding_match.span()[1] + right_match.span()[0] + len(str(right_num))):]

        right_part = f"{right_part_1}{right_num + exploding_pair_right_value}{right_part_2}"
    else:
        right_part = sn_string[exploding_match.span()[1]:]

    return eval(f"{left_part}0{right_part}")


def split_snailfish_number(sn: SNAILFISH_NUMBER) -> SNAILFISH_NUMBER:
    sn_string = list_to_string(sn)

    split_matches = list(re.finditer(r"\d{2,3}", sn_string))
    if not split_matches:
        raise NO_MORE_SPLIT_EXCEPTION

    # First match is the one on the leftmost-side
    split_match = split_matches[0]
    split_num = int(split_match.group(0))

    left_part = sn_string[:split_match.span()[0]]
    right_part = sn_string[split_match.span()[1]:]

    splitted_num_part: List[int] = []
    splitted_num_part.append(split_num // 2)
    splitted_num_part.append(math.ceil(split_num / 2))

    return eval(f"{left_part}{list_to_string(splitted_num_part)}{right_part}")


def reduce_snailfish_number(sn: SNAILFISH_NUMBER):
    done_something = True
    while done_something:
        try:
            sn = explode_snailfish_number(sn)
            done_something = True
            continue
        except NO_MORE_EXPLOSION_EXCEPTION:
            done_something = False

        try:
            sn = split_snailfish_number(sn)
            done_something = True
            continue
        except NO_MORE_SPLIT_EXCEPTION:
            done_something = False

    return sn


def calculate_magnitude(sn: SNAILFISH_NUMBER) -> int:
    pattern = r"(\[\d{1,10},\d{1,10}\])"

    sn_string = list_to_string(sn)
    while True:
        matches = list(re.finditer(pattern, sn_string))
        if not matches:
            break

        for match in matches:
            left, right = eval(match.group(0))
            sn_string = re.sub(re.escape(match.group(0)), str(left*3 + right*2), sn_string)

    return int(sn_string)


def test_boom():
    assert explode_snailfish_number(eval("[[[[[9,8],1],2],3],4]")) == eval("[[[[0,9],2],3],4]")
    assert explode_snailfish_number(eval("[7,[6,[5,[4,[3,2]]]]]")) == eval("[7,[6,[5,[7,0]]]]")
    assert explode_snailfish_number(eval("[[6,[5,[4,[3,2]]]],1]")) == eval("[[6,[5,[7,0]]],3]")
    assert explode_snailfish_number(eval("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")) == eval("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    assert explode_snailfish_number(eval("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")) == eval("[[3,[2,[8,0]]],[9,[5,[7,0]]]]")


def test_split():
    assert split_snailfish_number(eval("[[[[0,7],4],[15,[0,13]]],[1,1]]")) == eval("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    assert split_snailfish_number(eval("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")) == eval("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")


def test_multiple_steps():
    sn = eval("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    sn = explode_snailfish_number(sn)
    assert sn == eval("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
    sn = explode_snailfish_number(sn)
    assert sn == eval("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    sn = split_snailfish_number(sn)
    assert sn == eval("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    sn = split_snailfish_number(sn)
    assert sn == eval("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
    sn = explode_snailfish_number(sn)
    assert sn == eval("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


def test_reducing():
    assert reduce_snailfish_number(eval("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")) == eval("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")


def test():
    test_boom()
    test_split()
    test_multiple_steps()
    test_reducing()


@timer
def do_fancy_math(numbers: List[SNAILFISH_NUMBER]) -> int:
    d = deque(numbers)

    while len(d) > 1:
        num1 = d.popleft()
        num2 = d.popleft()

        addition_num = [num1, num2]
        reduced_addition_num = reduce_snailfish_number(addition_num)
        d.appendleft(reduced_addition_num)

    res = d.popleft()
    return calculate_magnitude(res)


@timer
def even_more_fancy_math(numbers: List[SNAILFISH_NUMBER]) -> int:
    highest = 0
    for perm in permutations(numbers, r=2):
        magnitude = calculate_magnitude(reduce_snailfish_number([*perm]))

        if magnitude > highest:
            highest = magnitude

    return highest


@timer
def parse_input():
    return [eval(sn) for sn in get_input_data(day=18).splitlines()]


if __name__ == "__main__":
    # test()
    numbers = parse_input()

    print(do_fancy_math(numbers))
    print(even_more_fancy_math(numbers))
