from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[List[int]]:
    result: List[List[int]] = []
    for line in in_str.split("\n")[:-1]:
        result.append([int(x) for x in list(line)])
    return result


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def get_adjacent_indices(
    point: Tuple[int, int], puzzle: List[List[int]]
) -> List[Union[Tuple[int, int], Tuple[None, None]]]:
    row_idx, col_idx = point
    top = (row_idx - 1, col_idx) if row_idx - 1 >= 0 else (None, None)
    bottom = (row_idx + 1, col_idx) if row_idx + 1 < len(puzzle) else (None, None)
    left = (row_idx, col_idx - 1) if col_idx - 1 >= 0 else (None, None)
    right = (
        (row_idx, col_idx + 1) if col_idx + 1 < len(puzzle[row_idx]) else (None, None)
    )
    top_right = (
        (row_idx - 1, col_idx + 1)
        if col_idx + 1 < len(puzzle[row_idx]) and row_idx - 1 >= 0
        else (None, None)
    )
    top_left = (
        (row_idx - 1, col_idx - 1)
        if col_idx - 1 >= 0 and row_idx - 1 >= 0
        else (None, None)
    )
    bottom_left = (
        (row_idx + 1, col_idx - 1)
        if row_idx + 1 < len(puzzle) and col_idx - 1 >= 0
        else (None, None)
    )
    bottom_right = (
        (row_idx + 1, col_idx + 1)
        if row_idx + 1 < len(puzzle) and col_idx + 1 < len(puzzle[row_idx])
        else (None, None)
    )

    return [top, bottom, left, right, top_right, top_left, bottom_left, bottom_right]


def simulate_step(puzzle: List[List[int]]) -> Tuple[List[List[int]], int]:
    already_flashed: List[List[bool]] = []
    for row_idx, row in enumerate(puzzle):
        already_flashed_row = []
        for col_idx, ele in enumerate(row):
            puzzle[row_idx][col_idx] = ele + 1
            already_flashed_row.append(False)
        already_flashed.append(already_flashed_row)

    total_flashes = 0
    while any([ele > 9 for row in puzzle for ele in row]):
        num_flashes = 0
        for row_idx, row in enumerate(puzzle):
            for col_idx, ele in enumerate(puzzle[row_idx]):
                adjacent = get_adjacent_indices((row_idx, col_idx), puzzle)
                if ele > 9:
                    puzzle[row_idx][col_idx] = 0
                    if not already_flashed[row_idx][col_idx]:
                        already_flashed[row_idx][col_idx] = True
                        num_flashes += 1
                        for (x, y) in adjacent:
                            if x is not None and y is not None:
                                if already_flashed[x][y]:
                                    puzzle[x][y] = 0
                                else:
                                    puzzle[x][y] += 1
        total_flashes += num_flashes
    return (puzzle, total_flashes)


def part_one(puzzle: List[List[int]]) -> int:
    total_flashes = 0
    for _ in range(100):
        next_puzzle, num_flashes = simulate_step(puzzle)
        puzzle = next_puzzle
        total_flashes += num_flashes
    return total_flashes


dummy_result = part_one(dummy_input.copy())
assert dummy_result == 1656, dummy_result
print(f"Part 1: {part_one(puzzle_input.copy())}")


def part_two(puzzle: List[List[int]]) -> int:
    i = 0
    while True:
        next_puzzle, _ = simulate_step(puzzle)
        if all([True if ele == 0 else False for row in puzzle for ele in row]):
            return i + 1
        puzzle = next_puzzle
        i += 1


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)

dummy_result = part_two(dummy_input.copy())
assert dummy_result == 195, dummy_result
print(f"Part 2: {part_two(puzzle_input.copy())}")
