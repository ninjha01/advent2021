from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[Tuple[str, str]]:
    res = []
    for x in in_str.strip().split("\n"):
        res.append(x.split("-"))
    return res


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def is_small_cave(cave: str) -> bool:
    return all([ord(letter) >= ord("a") and ord(letter) <= ord("z") for letter in cave])


def part_one(puzzle: List[Tuple[str, str]]) -> int:
    path_map = defaultdict(lambda: set())
    for (in_cave, out_cave) in puzzle:
        path_map[in_cave].add(out_cave)
        path_map[out_cave].add(in_cave)

    end_paths = set()
    paths = [["start"]]
    for _ in range(0, 10):
        new_paths = []
        for p in paths:
            curr_cave = p[-1]
            next_caves = path_map[curr_cave]
            for next_cave in next_caves:
                if is_small_cave(next_cave) and next_cave in p:
                    continue
                elif next_cave == "end":
                    end_paths.add(tuple(p + [next_cave]))
                else:
                    new_paths.append(p + [next_cave])
        paths = new_paths
    return len(end_paths)


dummy_result = part_one(dummy_input)
assert dummy_result == 10, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def can_visit_cave(cave: str, path: List[str]) -> bool:
    if cave == "start":
        return False
    elif not is_small_cave(cave):
        return True
    else:
        small_cave_count_map = defaultdict(lambda: 0)
        for path_cave in path:
            if is_small_cave(path_cave):
                small_cave_count_map[path_cave] += 1
        if small_cave_count_map[cave] > 2:
            raise ValueError("Visited cave more than twice!")
        elif small_cave_count_map[cave] == 2:
            return False
        elif small_cave_count_map[cave] == 1:
            # all others must be visited once or less
            return all(
                [
                    count < 2
                    for key, count in small_cave_count_map.items()
                    if key is not cave
                ]
            )
        # if visited zero times we can visit
        else:
            return True


def part_two(puzzle: List[Tuple[str, str]]) -> int:
    path_map = defaultdict(lambda: set())
    for (in_cave, out_cave) in puzzle:
        path_map[in_cave].add(out_cave)
        path_map[out_cave].add(in_cave)

    end_paths = set()
    paths = [["start"]]
    for _ in range(0, 15):
        new_paths = []
        for p in paths:
            curr_cave = p[-1]
            next_caves = path_map[curr_cave]
            for next_cave in next_caves:
                if next_cave == "end":
                    end_paths.add(tuple(p + [next_cave]))
                else:
                    if can_visit_cave(next_cave, p):
                        new_paths.append(p + [next_cave])
        paths = new_paths
    return len(end_paths)


dummy_result = part_two(dummy_input)
assert dummy_result == 36, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
