from typing import List

dummy_input_str = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
dummy_input = [x.split(" ") for x in dummy_input_str.split("\n")]

puzzle_input = [x.split(" ") for x in open("./input.txt").readlines()]


def part_one(puzzle: List[List[str]]) -> int:
    horiz = 0
    depth = 0
    for direction, raw_magnitude in puzzle:
        magnitude = int(raw_magnitude)
        if direction == "forward":
            horiz += magnitude
        elif direction == "up":
            depth -= magnitude
        elif direction == "down":
            depth += magnitude
        else:
            raise ValueError(f"Unexpected direction {direction}")
    return horiz * depth


assert part_one(dummy_input) == 150
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(puzzle: List[List[str]]) -> int:
    horiz = 0
    depth = 0
    aim = 0
    for direction, raw_magnitude in puzzle:
        magnitude = int(raw_magnitude)
        if direction == "forward":
            horiz += magnitude
            depth += aim * magnitude
        elif direction == "up":
            aim -= magnitude
        elif direction == "down":
            aim += magnitude
        else:
            raise ValueError(f"Unexpected direction {direction}")
    return horiz * depth


assert part_two(dummy_input) == 900, part_two(dummy_input)
print(f"Part 2: {part_two(puzzle_input)}")
