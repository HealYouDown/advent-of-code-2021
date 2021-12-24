from typing import List
from utils import get_input_data


class Instruction:
    def __init__(self, action: str, params: List[str]) -> None:
        self.action = action
        self.params = params

    @classmethod
    def from_line(cls, line: str) -> "Instruction":
        action, *params = line.split(" ")
        return Instruction(action, params)


class ALU:
    def __init__(self, input_buffer: List[int]) -> None:
        self.register = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self._input_buffer = input_buffer
        self.get_rv = lambda b: int(b) if b not in self.register else self.register[b]

    def process_instruction(self, instruction: Instruction) -> None:
        getattr(self, f"_process_{instruction.action}")(instruction)

    def _process_inp(self, instruction: Instruction) -> None:
        a, = instruction.params
        self.register[a] = self._input_buffer.pop(0)

    def _process_add(self, instruction: Instruction) -> None:
        a, b = instruction.params
        self.register[a] += self.get_rv(b)

    def _process_mul(self, instruction: Instruction) -> None:
        a, b = instruction.params
        self.register[a] *= self.get_rv(b)

    def _process_div(self, instruction: Instruction) -> None:
        a, b = instruction.params
        self.register[a] = self.register[a] // self.get_rv(b)

    def _process_mod(self, instruction: Instruction) -> None:
        a, b = instruction.params
        self.register[a] = self.register[a] % self.get_rv(b)

    def _process_eql(self, instruction: Instruction) -> None:
        a, b = instruction.params
        self.register[a] = 1 if self.register[a] == self.get_rv(b) else 0

if __name__ == "__main__":
    m0nad_instructions = [Instruction.from_line(line) for line in get_input_data(day=24).splitlines()]

    # all numbers, e.g. 99_999_999_999_999, ..., 33_333_333_333_333
    # 9s: {'w': 9, 'x': 1, 'y': 22, 'z': 7645130736}
    # 8s: {'w': 8, 'x': 1, 'y': 21, 'z': 7323858329}
    # 7s: {'w': 7, 'x': 1, 'y': 20, 'z': 7002585922}
    # 6s: {'w': 6, 'x': 1, 'y': 19, 'z': 6681313515}
    # 5s: {'w': 5, 'x': 1, 'y': 18, 'z': 6360041108}
    # 4s: {'w': 4, 'x': 1, 'y': 17, 'z': 6038768701}
    # 3s: {'w': 3, 'x': 1, 'y': 16, 'z': 5717496294}
    # 2s: {'w': 2, 'x': 1, 'y': 15, 'z': 5396223887}
    # 1s: {'w': 1, 'x': 1, 'y': 14, 'z': 5074951480}

    # 11111112387751 {'w': 1, 'x': 0, 'y': 0, 'z': 195190442}
    # 11111112387762 {'w': 2, 'x': 0, 'y': 0, 'z': 195190442}
    # 11111112387773 {'w': 3, 'x': 0, 'y': 0, 'z': 195190442}
    # 11111112387784 {'w': 4, 'x': 0, 'y': 0, 'z': 195190442}
    # 11111112387795 {'w': 5, 'x': 0, 'y': 0, 'z': 195190442}
    #             ^^
    model_numbers = range(99_999_999_999_999, 11_111_111_111_111, -10)

    for mn in model_numbers:
        if "0" in str(mn):
            continue

        alu = ALU(input_buffer=[int(i) for i in str(mn)])
        for instruction in m0nad_instructions:
            alu.process_instruction(instruction)

        print(mn, alu.register)
        if alu.register["z"] == 0:
            print("valid")
            break

