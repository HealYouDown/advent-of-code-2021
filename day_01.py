from utils import timer, get_input_data


@timer
def puzzle_1(data):
    increased_counter = 0

    previous_depth = None
    for idx, depth in enumerate(data):
        if idx > 0:
            if depth > previous_depth:
                increased_counter += 1
        previous_depth = depth

    return increased_counter


@timer
def puzzle_2(data):
    three_sums = []

    for i in range(len(data)):
        next_three_nums = data[i:i+3]
        if len(next_three_nums) != 3:
            break
        three_sums.append(sum(next_three_nums))

    increased_counter = 0

    previous_depth = None
    for idx, depth in enumerate(three_sums):
        if idx > 0:
            if depth > previous_depth:
                increased_counter += 1
        previous_depth = depth

    return increased_counter

if __name__ == "__main__":
    data = [int(i)
            for i in get_input_data(day=1).splitlines()]

    print(puzzle_1(data))
    print(puzzle_2(data))
