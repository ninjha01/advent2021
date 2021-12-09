from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """2199943210
3987894921
9856789892
8767896789
9899965678
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[List[int]]:
    result = []
    for y in in_str.split("\n")[:-1]:
        result.append([int(x) for x in list(y)])
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
    return [top, bottom, left, right]


def get_adjacent_values(
    point: Tuple[int, int], puzzle: List[List[int]]
) -> List[Optional[int]]:
    (
        (top_row, top_col),
        (bottom_row, bottom_col),
        (left_row, left_col),
        (right_row, right_col),
    ) = get_adjacent_indices(point, puzzle)
    top_val = (
        puzzle[top_row][top_col]
        if top_row is not None and top_col is not None
        else None
    )
    bottom_val = (
        puzzle[bottom_row][bottom_col]
        if bottom_row is not None and bottom_col is not None
        else None
    )
    left_val = (
        puzzle[left_row][left_col]
        if left_row is not None and left_col is not None
        else None
    )
    right_val = (
        puzzle[right_row][right_col]
        if right_row is not None and right_col is not None
        else None
    )
    return [top_val, bottom_val, left_val, right_val]


def find_low_points(puzzle: List[List[int]]) -> List[Tuple[int, int]]:
    low_points = []
    for row_idx in range(len(puzzle)):
        for col_idx, ele in enumerate(puzzle[row_idx]):
            top, bottom, left, right = get_adjacent_values(
                (row_idx, col_idx), puzzle=puzzle
            )
            if (
                (left is None or left > ele)
                and (right is None or right > ele)
                and (top is None or top > ele)
                and (bottom is None or bottom > ele)
            ):
                low_points.append((row_idx, col_idx))
    return low_points


def part_one(puzzle: List[List[int]]) -> int:
    low_points = find_low_points(puzzle)
    return sum([puzzle[row_idx][col_idx] + 1 for (row_idx, col_idx) in low_points])


dummy_result = part_one(dummy_input)
assert dummy_result == 15, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: List[List[int]]):
    def find_size_of_basin(point: Tuple[int, int]) -> int:
        points: Set[Tuple[int, int]] = set([point])
        prev_size = 0

        while prev_size < len(points):
            new_points = set()
            for (row_idx, col_idx) in points:
                top, bottom, left, right = get_adjacent_indices(
                    (row_idx, col_idx), puzzle=puzzle
                )
                top_val, bottom_val, left_val, right_val = get_adjacent_values(
                    (row_idx, col_idx), puzzle=puzzle
                )
                adjacent = {
                    top: top_val,
                    bottom: bottom_val,
                    left: left_val,
                    right: right_val,
                }
                for (x, y), val in adjacent.items():
                    if val is not None and val < 9:
                        if x is not None and y is not None and (x, y) not in points:
                            new_points.add((x, y))
            prev_size = len(points)
            [points.add(x) for x in new_points]
        return len(points)

    low_points = find_low_points(puzzle)
    find_size_of_basin(low_points[1])

    sizes = sorted([find_size_of_basin(point) for point in low_points], reverse=True)

    return sizes[0] * sizes[1] * sizes[2]


dummy_result = part_two(dummy_input)
assert dummy_result == 1134, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
