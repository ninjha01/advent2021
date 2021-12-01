from typing import List

dummy_input = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]


def part_one(puzzle: List[int]):
    increases = 0
    prev = puzzle[0]
    for curr in puzzle[1:]:
        if curr > prev:
            increases += 1
        prev = curr
    return increases


assert part_one(dummy_input) == 7
puzzle_input = [int(x.strip()) for x in open("./input.txt").readlines()]
print(f"Part 1: {part_one(puzzle_input)}")

def part_two(puzzle: List[int]):
    increases = 0
    start = 0
    end = 3
    prev_sum = sum(puzzle[start:end])
    while end <= len(puzzle):
        curr_sum = sum(puzzle[start:end])
        if curr_sum > prev_sum:
            increases += 1
        prev_sum = curr_sum
        start += 1
        end += 1
    return increases


assert part_two(dummy_input) == 5
print(f"Part 2: {part_two(puzzle_input)}")
