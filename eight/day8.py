from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import Dict, FrozenSet, List, Literal, Set, Tuple, Callable, Optional
from functools import cache
from statistics import median

dummy_input_str = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
puzzle_input_str = open("./input.txt").read()


def parse_input(in_str: str) -> List[Tuple[List[str], List[str]]]:
    results: List[Tuple[List[str], List[str]]] = []
    for line in in_str.split("\n"):
        if line == "":
            continue
        raw_input, raw_output = line.split(" | ")
        results.append((raw_input.split(" "), raw_output.split(" ")))
    return results


dummy_input = parse_input(dummy_input_str)
puzzle_input = parse_input(puzzle_input_str)


def determine_digit(signal_str: str) -> Optional[int]:
    if len(signal_str) == 2:
        return 1
    elif len(signal_str) == 4:
        return 4
    elif len(signal_str) == 3:
        return 7
    elif len(signal_str) == 7:
        return 8
    else:
        return None


def part_one(puzzle: List[Tuple[List[str], List[str]]]) -> int:
    count = 0
    for (_, out_signals) in puzzle:
        for out in out_signals:
            if determine_digit(out):
                count += 1
    return count


dummy_result = part_one(dummy_input)
assert dummy_result == 26, dummy_result
print(f"Part 1: {part_one(puzzle_input)}")


def determine_signal_mapping(in_signals: List[str]) -> Dict[str, str]:
    seg_count_map: Dict[str, int] = defaultdict(lambda: 0)
    four_sig = None
    one_sig = None
    seven_sig = None
    for in_sig in in_signals:
        if len(in_sig) == 4:
            four_sig = in_sig
        elif len(in_sig) == 2:
            one_sig = in_sig
        elif len(in_sig) == 3:
            seven_sig = in_sig
        for seg in list(in_sig):
            seg_count_map[seg] += 1
    seg_map = {}
    for seg, count in seg_count_map.items():
        if count == 8:  # to or tr
            if seg in seven_sig and seg not in one_sig:
                seg_map[seg] = "to"
            else:
                seg_map[seg] = "tr"
        elif count == 6:
            seg_map[seg] = "tl"
        elif count == 4:
            seg_map[seg] = "bl"
        elif count == 9:  # br
            seg_map[seg] = "br"
        elif count == 7:  # bo or md
            if seg in four_sig and seg not in one_sig:
                seg_map[seg] = "md"
            else:
                seg_map[seg] = "bo"
    return seg_map


def get_digit_from_sig_set(sig_set: FrozenSet[str]) -> str:
    digit_map: Dict[FrozenSet[str], str] = {
        frozenset(["to", "tl", "tr", "bl", "br", "bo"]): "0",
        frozenset(["tr", "br"]): "1",
        frozenset(["to", "tr", "md", "bl", "bo"]): "2",
        frozenset(["to", "tr", "md", "br", "bo"]): "3",
        frozenset(["tl", "tr", "md", "br"]): "4",
        frozenset(["to", "tl", "md", "br", "bo"]): "5",
        frozenset(["to", "tl", "md", "bl", "br", "bo"]): "6",
        frozenset(["to", "tr", "br"]): "7",
        frozenset(["to", "tl", "tr", "md", "bl", "br", "bo"]): "8",
        frozenset(["to", "tl", "tr", "md", "br", "bo"]): "9",
    }
    return digit_map[sig_set]


def part_two(puzzle: List[Tuple[List[str], List[str]]]) -> int:
    out_nums: List[int] = []
    for (in_signals, out_signals) in puzzle:
        sig_map = determine_signal_mapping(in_signals)
        out_num: List[str] = []
        for out_sig in out_signals:
            mapped_sigs = frozenset([sig_map[sig] for sig in list(out_sig)])
            out_num.append(get_digit_from_sig_set(mapped_sigs))
        out_nums.append(int("".join(out_num)))
    return sum(out_nums)


dummy_result = part_two(dummy_input)
assert dummy_result == 61229, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
