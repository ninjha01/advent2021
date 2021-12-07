from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List, Literal, Set, Tuple, Callable
from functools import cache
from statistics import median

dummy_input_str = """16,1,2,0,4,2,7,1,2,14
"""

puzzle_input_str = open("./input.txt").read()

dummy_input = [int(x) for x in dummy_input_str.split(",")]
puzzle_input = [int(x) for x in puzzle_input_str.split(",")]


def get_frequency_map(num_list: List[int]) -> Dict[int, int]:
    freq_map = defaultdict(lambda: 0)
    for num in num_list:
        freq_map[num] += 1
    return freq_map


def get_weighted_average(num_list: List[int], cost_func: Callable[[int], int]) -> int:
    weights = [cost_func(num) for num in num_list]
    return round(
        sum(num * weight for num, weight in zip(num_list, weights)) / sum(weights)
    )


def part_one(puzzle: List[int]) -> int:
    freq_map = get_frequency_map(puzzle)

    def get_cost(freq_map: Dict[int, int], num: int) -> int:
        cost = 0
        for curr_num, count in freq_map.items():
            cost += abs(curr_num - num) * count
        return cost

    cost_list = [get_cost(freq_map, num) for num in puzzle]
    return min(cost_list)


dummy_result = part_one(dummy_input)
assert dummy_result == 37, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: List[int]) -> int:
    freq_map = get_frequency_map(puzzle)

    def get_cost(freq_map: Dict[int, int], num: int) -> int:
        cost = 0
        for curr_num, count in freq_map.items():
            distance = abs(curr_num - num)

            def get_cost_per_count(distance: int) -> int:
                return distance * (distance + 1) // 2

            cost += get_cost_per_count(distance) * count
        return cost

    cost_list = [get_cost(freq_map, num) for num in range(min(puzzle), max(puzzle))]
    return min(cost_list)


dummy_result = part_two(dummy_input)
assert dummy_result == 168, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
