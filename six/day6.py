from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List, Literal, Set, Tuple

dummy_input_str = """3,4,3,1,2
"""

puzzle_input_str = open("./input.txt").read()

dummy_input = [int(x) for x in dummy_input_str.split(",")]
puzzle_input = [int(x) for x in puzzle_input_str.split(",")]


def simulate_fish(puzzle: List[int], num_of_days: int):
    fish_count_map = {k: 0 for k in range(0, 9)}
    for timer in puzzle:
        fish_count_map[timer] += 1
    for i in range(num_of_days):
        new_fish_map = {k: 0 for k in range(0, 9)}
        for timer, count in fish_count_map.items():
            if timer == 0:
                # reset fish timer
                new_fish_map[8] += count
                # Create baby fish
                new_fish_map[6] += count
            else:
                new_fish_map[timer - 1] += count
        fish_count_map = new_fish_map
    return sum(fish_count_map.values())


def part_one(puzzle: List[int]):
    return simulate_fish(puzzle, 80)


dummy_result = part_one(dummy_input)
assert dummy_result == 5934, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: List[int]):
    return simulate_fish(puzzle, 256)


dummy_result = part_two(dummy_input)
assert dummy_result == 26984457539, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
