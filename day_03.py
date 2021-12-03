from typing import List
from utils import timer, get_input_data


def count_one_bit_positions(data):
    # Counts the 1 bits for each position
    counter = [0 for _ in range(len(data[0]))]

    for bit_repr in data:
        for idx, bit in enumerate(bit_repr):
            counter[idx] += int(bit)

    return counter


@timer
def puzzle_1(data):
    data_length = len(data)
    one_bit_counter = count_one_bit_positions(data)

    gamma_rate_bits = [1 if (count > data_length/2) else 0
                       for count in one_bit_counter]
    epsilon_rate_bits = [0 if b == 1 else 1
                         for b in gamma_rate_bits]

    gamma_rate = int("".join([str(b) for b in gamma_rate_bits]), 2)
    epsilon_rate = int("".join([str(b) for b in epsilon_rate_bits]), 2)

    return gamma_rate * epsilon_rate


@timer
def puzzle_2(data: List[str]):
    # Clone data
    oxygen_numbers = list(data)
    co2_numbers = list(data)

    for pos in range(len(data[0])):
        # Oxygen
        if len(oxygen_numbers) > 1:
            ox_bit_counter = count_one_bit_positions(oxygen_numbers)
            mc_bit = (1
                    if (ox_bit_counter[pos] > len(oxygen_numbers)/2
                        or ox_bit_counter[pos] == len(oxygen_numbers)/2)
                    else 0)

            oxygen_numbers = [num for num in oxygen_numbers
                            if int(num[pos]) == mc_bit]

        # Co2
        if len(co2_numbers) > 1:
            co_bit_counter = count_one_bit_positions(co2_numbers)
            lc_bit = (0
                    if (co_bit_counter[pos] > len(co2_numbers)/2
                        or co_bit_counter[pos] == len(co2_numbers)/2)
                    else 1)
            co2_numbers = [num for num in co2_numbers
                           if int(num[pos]) == lc_bit]

    oxygen_generator_rate = int(oxygen_numbers[0], 2)
    co2_scrubbing_rate = int(co2_numbers[0], 2)

    return oxygen_generator_rate * co2_scrubbing_rate


if __name__ == "__main__":
    data = [bit_repr for bit_repr in get_input_data(day=3).splitlines()]

    print(puzzle_1(data))
    print(puzzle_2(data))
