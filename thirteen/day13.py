from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    dots: List[Tuple[int, int]] = []
    folds: List[Tuple[int, int]] = []
    for line in in_str.split("\n")[:-1]:
        if "," in line:
            split = line.strip().split(",")
            dots.append((int(split[0]), int(split[1])))
        elif "fold" in line:
            fold = int(line.strip().split("=")[-1])
            fold_line = (fold, 0) if "x" in line else (0, fold)
            folds.append(fold_line)
    return (dots, folds)


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def print_sheet(dots: List[Tuple[int, int]]):
    max_x = max([d[0] for d in dots])
    max_y = max([d[1] for d in dots])
    dots_set = set(dots)
    print_buffer = []
    for row_idx in range(max_y + 1):
        print_buffer_row = []
        for col_idx in range(max_x + 1):
            marker = "#" if (col_idx, row_idx) in dots_set else "."
            print_buffer_row.append(marker)
        print_buffer.append("".join(print_buffer_row))
    print("\n".join(print_buffer))


def part_one(puzzle: Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]) -> int:
    dots, folds = puzzle
    new_dots = set()
    for fold in folds[:1]:
        fold_axis: Literal["x", "y"] = "x" if fold[1] == 0 else "y"
        fold_mag = fold[0] if fold_axis == "x" else fold[1]
        for (x, y) in dots:
            folded_dot = None
            new_x = x
            new_y = y
            if fold_axis == "y" and y > fold_mag:
                new_y = fold_mag - (y - fold_mag)
            elif fold_axis == "x" and x > fold_mag:
                new_x = fold_mag - (x - fold_mag)
            folded_dot = (new_x, new_y)
            new_dots.add(folded_dot)
        dots = list(new_dots)
    return len(dots)


dummy_result = part_one(dummy_input)
assert dummy_result == 17, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]):
    dots, folds = puzzle
    for fold in folds:
        new_dots = set()
        fold_axis: Literal["x", "y"] = "x" if fold[1] == 0 else "y"
        fold_mag = fold[0] if fold_axis == "x" else fold[1]
        for (x, y) in dots:
            folded_dot = None
            new_x = x
            new_y = y
            if fold_axis == "y" and y > fold_mag:
                new_y = fold_mag - (y - fold_mag)
            elif fold_axis == "x" and x > fold_mag:
                new_x = fold_mag - (x - fold_mag)
            folded_dot = (new_x, new_y)
            new_dots.add(folded_dot)
        dots = list(new_dots)
    print_sheet(dots)


print("Should be `0`: ")
part_two(dummy_input)
print("Should be `AHPRPAUZ`: ")
part_two(puzzle_input)
