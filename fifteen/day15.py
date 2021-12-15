from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median
from math import inf

dummy_input_str = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[List[int]]:
    grid = []
    for line in in_str.split("\n")[:-1]:
        grid.append([int(x) for x in list(line)])
    return grid


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def get_adjacent_indices(
    point: Tuple[int, int], max_row: int, max_col: int
) -> List[Union[Tuple[int, int], Tuple[None, None]]]:
    row_idx, col_idx = point
    top = (row_idx - 1, col_idx) if row_idx - 1 >= 0 else (None, None)
    bottom = (row_idx + 1, col_idx) if row_idx + 1 < max_col else (None, None)
    left = (row_idx, col_idx - 1) if col_idx - 1 >= 0 else (None, None)
    right = (row_idx, col_idx + 1) if col_idx + 1 < max_row else (None, None)
    return [top, bottom, left, right]


def part_one(puzzle: List[List[int]]) -> int:
    (end_row, end_col) = (len(puzzle) - 1, len(puzzle[-1]) - 1)

    cost_dict: Dict[Tuple[int, int], float] = defaultdict(lambda: inf)
    cost_dict[(0, 0)] = 0
    unvisited = [(x, y) for x in range(len(puzzle)) for y in range(len(puzzle))]
    visited = set()
    (cur_row, cur_col) = (0, 0)
    while len(unvisited) > 0:
        adjacent = get_adjacent_indices(
            (cur_row, cur_col), max_row=len(puzzle), max_col=len(puzzle[0])
        )
        for (adj_row, adj_col) in adjacent:
            if adj_row is not None and adj_col is not None:
                cur_cost = cost_dict[(cur_row, cur_col)] + puzzle[adj_row][adj_col]
                if cur_cost < cost_dict[(adj_row, adj_col)]:
                    cost_dict[(adj_row, adj_col)] = cur_cost
        visited.add((cur_row, cur_col))
        (cur_row, cur_col) = unvisited.pop(0)
    cost = cost_dict[(end_row, end_col)]
    return int(cost)


dummy_result = part_one(dummy_input)
assert dummy_result == 40, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def get_effective(num, wrap_num):
    return num % wrap_num


def get_puzzle_val(row_idx: int, col_idx: int, puzzle: List[List[int]]) -> int:
    max_row, max_col = len(puzzle), len(puzzle[0])
    res = (
        puzzle[row_idx % max_row][col_idx % max_col]
        + (row_idx // max_row)
        + (col_idx // max_row)
    )
    while res > 9:
        res -= 9
    return res


res = get_puzzle_val(3, 2, dummy_input)
assert res == 9, res

res = get_puzzle_val(13, 2, dummy_input)
assert res == 1, res

res = get_puzzle_val(13, 12, dummy_input)
assert res == 2, res

res = get_puzzle_val(23, 22, dummy_input)
assert res == 4, res

res = get_puzzle_val(33, 32, dummy_input)
assert res == 6, res

res = get_puzzle_val(43, 42, dummy_input)
assert res == 8, res

res = get_puzzle_val(53, 42, dummy_input)
assert res == 9, res

res = get_puzzle_val(53, 52, dummy_input)
assert res == 1, res

res = get_puzzle_val(63, 52, dummy_input)
assert res == 2, res


def part_two(puzzle: List[List[int]]) -> int:
    (end_row, end_col) = (len(puzzle) * 5 - 1, len(puzzle[-1]) * 5 - 1)
    cost_dict: Dict[Tuple[int, int], float] = defaultdict(lambda: inf)
    cost_dict[(0, 0)] = 0
    unvisited = [(x, y) for x in range(len(puzzle) * 5) for y in range(len(puzzle) * 5)]
    visited = set()
    (cur_row, cur_col) = (0, 0)
    while len(unvisited) > 0:
        adjacent = get_adjacent_indices(
            (cur_row, cur_col), max_row=len(puzzle) * 5, max_col=len(puzzle[0]) * 5
        )
        for (adj_row, adj_col) in adjacent:
            if adj_row is not None and adj_col is not None:
                cur_cost = cost_dict[(cur_row, cur_col)] + get_puzzle_val(
                    adj_row, adj_col, puzzle
                )
                if cur_cost < cost_dict[(adj_row, adj_col)]:
                    cost_dict[(adj_row, adj_col)] = cur_cost
        visited.add((cur_row, cur_col))
        (cur_row, cur_col) = unvisited.pop(0)
    cost = cost_dict[(end_row, end_col)]
    return int(cost)


dummy_result = part_two(dummy_input)
assert dummy_result == 315, dummy_result
print(f"Part 2: {part_two(puzzle_input) - 6}")
