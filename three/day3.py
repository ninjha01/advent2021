from typing import List, Literal, Set

dummy_input_str = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
dummy_input = dummy_input_str.split("\n")

puzzle_input = [x.strip() for x in open("./input.txt").readlines()]


def part_one(puzzle: List[str]) -> int:
    most_common = []
    least_common = []
    for i in range(len(puzzle[0])):
        num_0 = 0
        num_1 = 0
        for p in puzzle:
            if p[i] == "0":
                num_0 += 1
            elif p[i] == "1":
                num_1 += 1
            else:
                raise ValueError(f"Unexpected digit '{p[i]}'")
        if num_0 > num_1:
            most_common.append("0")
            least_common.append("1")
        else:
            most_common.append("1")
            least_common.append("0")
    gamma_str, epsilon_str = "".join(most_common), "".join(least_common)
    gamma = int(gamma_str, 2)
    epsilon = int(epsilon_str, 2)
    return gamma * epsilon


assert part_one(dummy_input) == 198
print(f"Part 1: {part_one(puzzle_input)}")


def find_rating(puzzle: List[str], rating_type: Literal["O2", "CO2"]) -> int:
    candidates = set(puzzle)

    def filter_candidates(candidates: Set[str], candidates_to_remove: List[str]):
        for c in candidates_to_remove:
            if c in candidates:
                candidates.remove(c)

    for i in range(len(puzzle[0])):
        candidates_with_zero_at_ith_pos = list(
            filter(lambda x: x[i] == "0", candidates)
        )
        candidates_with_one_at_ith_pos = list(filter(lambda x: x[i] == "1", candidates))
        have_more_zeros = len(candidates_with_zero_at_ith_pos) > len(
            candidates_with_one_at_ith_pos
        )
        if have_more_zeros:
            if rating_type == "O2":
                filter_candidates(candidates, candidates_with_one_at_ith_pos)
            elif rating_type == "CO2":
                filter_candidates(candidates, candidates_with_zero_at_ith_pos)
            else:
                raise ValueError(f"Unexpected rating type {rating_type}")
        else:
            if rating_type == "O2":
                filter_candidates(candidates, candidates_with_zero_at_ith_pos)
            elif rating_type == "CO2":
                filter_candidates(candidates, candidates_with_one_at_ith_pos)
            else:
                raise ValueError(f"Unexpected rating type {rating_type}")
        if len(candidates) == 1:
            return int(candidates.pop(), 2)
    raise ValueError("Expected to eliminate all but one candidate")


def part_two(puzzle: List[str]) -> int:
    o2_rating = find_rating(puzzle, "O2")
    cO2_rating = find_rating(puzzle, "CO2")
    return o2_rating * cO2_rating


assert part_two(dummy_input) == 230, part_two(dummy_input)
print(f"Part 2: {part_two(puzzle_input)}")
