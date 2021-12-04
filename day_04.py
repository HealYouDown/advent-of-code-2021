from itertools import chain
from typing import List, Tuple

from utils import get_input_data, timer


class BingoField:
    def __init__(self, numbers: List[int]) -> None:
        # the bingo field numbers are stored in a list of sequential numbers,
        # no 2D grid
        self._numbers: List[int] = numbers

        # The actual bingo field however is just an array with 25 False values
        # to keep track of which number was called
        self._tracking: List[bool] = [False for _ in range(len(self._numbers))]

    def call_number(self, number: int) -> bool:
        """Calls a number for the board

        Args:
            number (int): The number to call out.

        Returns:
            bool: True if the number was found in the board, else False
        """
        if number not in self._numbers:
            return False

        self._tracking[self._numbers.index(number)] = True

        return True

    def check_winning(self) -> bool:
        """Checks if the board has a winning set, either horizontally or
        vertically.

        Returns:
            bool: [description]
        """
        if self._tracking.count(True) < 5:
            return False

        # Checks horizontal lines
        for i in range(0, 25, 5):
            row = self._tracking[i:i+5]
            if row.count(True) == 5:
                return True

        # Check vertical lines
        for i in range(0, 5, 1):
            column = [self._tracking[i + j*5] for j in range(5)]
            if column.count(True) == 5:
                return True

        return False

    def calculate_unmarked_sum(self) -> int:
        """Calculates the sum of all unmarked numbers on the bingo field.

        Returns:
            int: The sum of all unmarked numbers.
        """
        return sum([num for i, num in enumerate(self._numbers)
                    if not self._tracking[i]])


@timer
def puzzle_1(bingo_fields: List[BingoField], bingo_numbers: List[int]):
    for number in bingo_numbers:
        for field in bingo_fields:
            field.call_number(number)
            if field.check_winning():
                return field.calculate_unmarked_sum() * number


@timer
def puzzle_2(bingo_fields: List[BingoField], bingo_numbers: List[int]):
    # Ordered list which stores the bingo fields that have won
    finished_fields: List[BingoField] = []
    # Stores the number that won the board for the same index as the board
    finished_numbers: List[int] = []

    for number in bingo_numbers:
        for field in bingo_fields:
            if field not in finished_fields:
                field.call_number(number)

                if field.check_winning():
                    finished_fields.append(field)
                    finished_numbers.append(number)

    return finished_fields[-1].calculate_unmarked_sum() * finished_numbers[-1]


@timer
def parse_input() -> Tuple[List[BingoField], List[int]]:
    input_data = get_input_data(day=4).splitlines()
    bingo_numbers = [int(i) for i in input_data[0].split(",")]
    # Read the fields as just a sequence of integers from which we will create
    # the bingo fields later
    field_numbers = list(chain.from_iterable(
        [[int(num) for num in line.split(" ") if num]
         for line in input_data[1:]
         if line]
    ))

    bingo_fields = [BingoField(field_numbers[i:i+25]) for i in range(0, len(field_numbers), 25)]

    return bingo_fields, bingo_numbers


if __name__ == "__main__":
    bingo_fields, bingo_numbers = parse_input()

    print(puzzle_1(bingo_fields, bingo_numbers))
    print(puzzle_2(bingo_fields, bingo_numbers))
