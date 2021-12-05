from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, List, Literal, Set, Tuple

dummy_input_str = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[Tuple[int, int, int, int]]:
    output = []
    for line in in_str.split("\n")[:-1]:
        start, end = line.split(" -> ")
        startx, starty = start.split(",")
        endx, endy = end.split(",")
        generated_line = (int(startx), int(starty), int(endx), int(endy))
        output.append(generated_line)
    return output


def solve_puzzle(puzzle: str, ignore_diagonals=True) -> int:
    lines = parse_input(puzzle)
    point_map: Dict[Tuple[int, int], int] = defaultdict(lambda: 0)
    for line in lines:
        x1, y1, x2, y2 = line
        # traverse line vertically
        if x1 == x2:
            start = min(y1, y2)
            distance = abs(y1 - y2)
            for i in range(0, distance + 1):
                point_map[(x1, start + i)] += 1
        # traverse line horiontally
        elif y1 == y2:
            start = min(x1, x2)
            distance = abs(x1 - x2)
            for i in range(0, distance + 1):
                point_map[(start + i, y1)] += 1
        else:
            if ignore_diagonals:
                continue
            else:
                x_step = 1 if x2 > x1 else -1
                y_step = 1 if y2 > y1 else -1
                for i in range(0, abs(x1 - x2) + 1):
                    covered_point = (x1 + i * x_step, y1 + i * y_step)
                    point_map[covered_point] += 1
    overlap_count = 0
    for val in point_map.values():
        if val >= 2:
            overlap_count += 1
    return overlap_count


def part_one(puzzle: str) -> int:
    return solve_puzzle(puzzle, ignore_diagonals=True)


dummy_result = part_one(dummy_input_str)
assert dummy_result == 5, dummy_result
print(f"Part 1: {part_one(puzzle_input_str)}")


def part_two(puzzle: str) -> int:
    return solve_puzzle(puzzle, ignore_diagonals=False)


dummy_result = part_two(dummy_input_str)
assert dummy_result == 12, dummy_result
print(f"Part 2: {part_two(puzzle_input_str)}")
