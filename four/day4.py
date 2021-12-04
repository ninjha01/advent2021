from typing import List, Literal, Set, Tuple, Dict
from dataclasses import dataclass

dummy_input_str = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

puzzle_input = open("./input.txt").read()


@dataclass
class BingoBoard:
    board: List[List[int]]
    marked_numbers: Dict[int, bool]
    unmarked_numbers: Dict[int, bool]

    def mark_number_if_have(self, num: int):
        if num in self.unmarked_numbers:
            self.marked_numbers[num] = self.unmarked_numbers[num]
            del self.unmarked_numbers[num]

    def has_won(self):
        # check rows
        for y in range(len(self.board)):
            num_marked = 0
            for i, num in enumerate(self.board[y]):
                if num in self.marked_numbers:
                    num_marked += 1
            if num_marked == len(self.board[y]):
                return True
        # check columns
        for x in range(len(self.board[0])):
            num_marked = 0
            for y in range(len(self.board)):
                ele = self.board[y][x]
                if ele in self.marked_numbers:
                    num_marked += 1
            if num_marked == len(self.board):
                return True
        return False

    def calculate_score(self, winning_number: int) -> int:
        return sum(self.unmarked_numbers.keys()) * winning_number


def parse_input(in_str: str) -> Tuple[List[int], List[BingoBoard]]:
    lines = in_str.split("\n")
    drawings = [int(x) for x in lines[0].split(",")]

    boards = []
    curr_board_list = []
    for l in lines[2:]:
        if l == "":
            unmarked_numbers = {}
            for y in range(len(curr_board_list)):
                for i, num in enumerate(curr_board_list[y]):
                    unmarked_numbers[num] = True
            boards.append(
                BingoBoard(
                    board=curr_board_list,
                    marked_numbers=dict(),
                    unmarked_numbers=unmarked_numbers,
                )
            )
            curr_board_list = []
        else:
            row = [int(x) for x in l.split(" ") if x != ""]
            curr_board_list.append(row)
    return drawings, boards


def part_one(in_str: str) -> int:
    drawings, boards = parse_input(in_str)
    for num in drawings:
        for b in boards:
            b.mark_number_if_have(num)
            if b.has_won():
                return b.calculate_score(num)
    return -1


assert part_one(dummy_input_str) == 4512, part_one(dummy_input_str)
print(f"Part 1: {part_one(puzzle_input)}")


def part_two(in_str: str) -> int:
    drawings, boards = parse_input(in_str)
    remaining_boards = boards.copy()
    for num in drawings:
        for b in boards:
            b.mark_number_if_have(num)
            if b.has_won():
                if len(remaining_boards) == 1:
                    losing_board = remaining_boards[0]
                    if losing_board.has_won():
                        return losing_board.calculate_score(num)
                if b in remaining_boards:
                    remaining_boards.remove(b)


dummy_result = part_two(dummy_input_str)
assert dummy_result == 1924, dummy_result
print(f"Part 2: {part_two(puzzle_input)}")
