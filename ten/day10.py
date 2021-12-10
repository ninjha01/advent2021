from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[List[str]]:
    return [list(x) for x in in_str.split("\n")][:-1]


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)

opener_closer_map = {"(": ")", "{": "}", "[": "]", "<": ">"}
closer_opener_map = {v: k for k, v in opener_closer_map.items()}


def part_one(puzzle: List[List[str]]) -> int:
    failures = []
    for line in puzzle:
        balance_stack = []
        for char in line:
            if char in opener_closer_map:
                balance_stack.append(char)
            elif char in closer_opener_map:
                if len(balance_stack) == 0:
                    break  # skip incomplete lines
                elif balance_stack[-1] == closer_opener_map[char]:
                    balance_stack.pop()
                else:
                    failures.append(char)
                    break
    score_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum([score_map[char] for char in failures])


dummy_result = part_one(dummy_input)
assert dummy_result == 26397, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: List[List[str]]) -> int:
    incompletes = []
    for line in puzzle:
        balance_stack = []
        corrupted = False
        for char in line:
            if char in opener_closer_map:
                balance_stack.append(char)
            elif char in closer_opener_map:
                if (
                    balance_stack[-1] == closer_opener_map[char]
                    and len(balance_stack) > 0
                ):  # Correctly closes
                    balance_stack.pop()
                else:  # Incorrectly closes
                    corrupted = True
                    break
        # If incomplete
        if not corrupted and len(balance_stack) > 0:
            incompletes.append(balance_stack)

    scores = []
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    for incomp in incompletes:
        completion_string = [opener_closer_map[char] for char in incomp[::-1]]
        score = 0
        for c in completion_string:
            score *= 5
            score += score_map[c]
        scores.append(score)
    scores = sorted(scores)
    return scores[len(scores) // 2]


dummy_result = part_two(dummy_input)
assert dummy_result == 288957, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
