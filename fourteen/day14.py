from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional, Union
from functools import cache
from statistics import median

dummy_input_str = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> Tuple[str, Dict[str, str]]:
    lines = in_str.split("\n")[:-1]
    start_str = lines[0]
    rules: Dict[str, str] = {}
    for line in lines[2:]:
        target, insertion = line.split(" -> ")
        rules[target] = insertion
    return (start_str, rules)


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def break_into_chunks(in_str: str) -> List[str]:
    chunks = []
    for i in range(len(in_str) - 1):
        chunks.append(in_str[i : i + 2])
    return chunks


def merge_chunks_into_string(chunks: List[str]) -> str:
    reconstituted = [x[:-1] for x in chunks] + [chunks[-1][-1]]
    return "".join(reconstituted)


def part_one(puzzle: Tuple[str, Dict[str, str]]) -> int:
    start_str, rules = puzzle
    for _ in range(0, 10):
        chunks = break_into_chunks(start_str)
        new_chunks: List[str] = []
        for chunk in chunks:
            insertion = rules.get(chunk, None)
            if insertion is not None:
                new_chunks.append("".join([chunk[0], insertion, chunk[1]]))
            else:
                new_chunks.append(chunk)
        new_str = merge_chunks_into_string(new_chunks)
        start_str = new_str
    count_dict = defaultdict(lambda: 0)
    for char in start_str:
        count_dict[char] += 1
    most_common = max(count_dict.values())
    least_common = min(count_dict.values())
    return most_common - least_common


dummy_result = part_one(dummy_input)
assert dummy_result == 1588, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: Tuple[str, Dict[str, str]]) -> int:
    start_str, rules = puzzle
    chunk_dict = defaultdict(lambda: 0)
    for chunk in break_into_chunks(start_str):
        chunk_dict[chunk] += 1
    for _ in range(0, 40):
        next_chunk_dict = defaultdict(lambda: 0)
        for chunk, count in chunk_dict.items():
            insertion = rules.get(chunk, None)
            if insertion is not None:
                start, end = chunk[0], chunk[1]
                next_chunk_dict[start + insertion] += count
                next_chunk_dict[insertion + end] += count
            else:
                next_chunk_dict[chunk] += count
        chunk_dict = next_chunk_dict

    count_map = defaultdict(lambda: 0)
    # start and end which are off by 1
    count_map[start_str[0]] += 1
    count_map[start_str[-1]] += 1

    # and counts are doubled
    for chunk, count in chunk_dict.items():
        count_map[chunk[0]] += count
        count_map[chunk[1]] += count
    count_map = {k: v // 2 for k, v in count_map.items()}

    most_common = max(count_map.values())
    least_common = min(count_map.values())
    return most_common - least_common


dummy_result = part_two(dummy_input)
assert dummy_result == 2188189693529, dummy_result
print(f"Part 1: {part_two(puzzle_input)}")
