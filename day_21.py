from utils import timer


class DeterministicDice:
    def __init__(self, sides: int):
        self._sides = sides
        self._count = 0

    @property
    def next_number(self) -> int:
        n = (self._count % self._sides) + 1
        self._count += 1

        return n

    @property
    def number_of_dice_rolls(self) -> int:
        return self._count

    def roll_n_times(self, n: int) -> int:
        return sum(self.next_number for _ in range(n))


class Player:
    def __init__(self, start_pos: int) -> None:
        self._pos = start_pos - 1
        self._max_pos = 10
        self._score = 0

    @property
    def pos(self) -> int:
        # Internally, the pos is stored as 0-9
        return self._pos + 1

    @property
    def score(self) -> int:
        return self._score

    def step(self, n: int) -> None:
        self._pos = (self._pos + n) % self._max_pos
        self._score += self.pos


@timer
def puzzle_1() -> int:
    dice = DeterministicDice(sides=100)
    p1 = Player(start_pos=6)
    p2 = Player(start_pos=7)

    while True:
        p1.step(dice.roll_n_times(3))
        if p1.score >= 1000:
            return p2.score * dice.number_of_dice_rolls
        
        p2.step(dice.roll_n_times(3))
        if p2.score >= 1000:
            return p1.score * dice.number_of_dice_rolls


def puzzle_2():
    pass


if __name__ == "__main__":
    print(puzzle_1())
