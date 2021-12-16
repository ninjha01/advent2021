from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
from typing import (
    Dict,
    FrozenSet,
    List,
    Literal,
    Set,
    Tuple,
    Callable,
    Optional,
    Union,
    TypeVar,
)
from functools import cache
from statistics import median
from math import inf

dummy_input_str = """38006F45291200"""
puzzle_input_str = open("./input.txt").read()

BinStr = Literal["0", "1"]
T = TypeVar("T")


@dataclass
class Packet:
    version: int
    type_id: int


@dataclass
class LiteralPacket(Packet):
    value: int


@dataclass
class OperatorPacket(Packet):
    length_type: Literal[0, 1]
    sub_packets: List[Packet]


def hex_str_to_bin(in_str: str) -> str:
    num = None
    if "0x" not in in_str:
        num = eval(f"0x{in_str}")
    else:
        num = eval(in_str)
    return ("0000" + bin(num)[2:])[-4:]


def pop_n(in_list: List[T], n: int) -> List[T]:
    results = []
    for _ in range(n):
        if len(in_list) > 0:
            results.append(in_list.pop(0))
    return results


def bit_list_to_int(bit_list: List[str]) -> int:
    return int("".join(bit_list), 2)


def parse_input(in_str: str) -> List[str]:
    return list("".join([hex_str_to_bin(x) for x in in_str]))


def bin_list_to_str(in_list: List[str]):
    padding = len(in_list) % 4
    in_list = ["0"] * padding + in_list
    out_list = []
    while in_list:
        curr_chunk = pop_n(in_list, 4)
        out_list.append("".join(curr_chunk))
    return " ".join(out_list)


def bit_list_to_packets(queued_bits: List[str]) -> List[Packet]:
    packets = []
    # print("Bits to parse: ", bin_list_to_str(queued_bits))
    # print("id", id(queued_bits))
    while len(queued_bits) > 10:
        header = pop_n(queued_bits, 6)
        bin_list_to_str(header)
        version = bit_list_to_int(header[:3])
        type_id = bit_list_to_int(header[3:])
        # print(f"{version=} {type_id=}")
        # input()
        # LiteralPacket
        if type_id == 4:
            # print(f"Parsing LiteralPacket v{version}")
            curr_chunk = pop_n(queued_bits, 5)
            val_bit_list = []
            while curr_chunk[0] == "1":
                val_bit_list.extend(curr_chunk[1:])
                curr_chunk = pop_n(queued_bits, 5)
            val_bit_list.extend(curr_chunk[1:])

            lit_packet = LiteralPacket(
                version=version, type_id=type_id, value=bit_list_to_int(val_bit_list)
            )
            # print(f"It had value {lit_packet.value}")
            packets.append(lit_packet)
        else:
            length_type_bits = pop_n(queued_bits, 1)
            length_type = bit_list_to_int(length_type_bits)
            assert length_type == 0 or length_type == 1
            # print(f"Parsing OperatorPacket v{version} l{length_type}")
            sub_packets = []
            remaining_packets = []
            if length_type == 0:
                num_bits_list = pop_n(queued_bits, 15)
                num_bits = bit_list_to_int(num_bits_list)
                # print(f"subpacket bit length {num_bits}")
                next_packets = pop_n(queued_bits, num_bits)
                sub_packets = bit_list_to_packets(next_packets)
            else:
                num_packets_bit_list = pop_n(queued_bits, 11)
                num_packets = bit_list_to_int(num_packets_bit_list)
                remaining_packets = bit_list_to_packets(queued_bits)
                sub_packets = pop_n(remaining_packets, num_packets)
            operator_packet = OperatorPacket(
                version=version,
                type_id=type_id,
                length_type=length_type,
                sub_packets=sub_packets,
            )
            packets.append(operator_packet)
            if len(remaining_packets):
                packets.extend(remaining_packets)
    return packets


def ver_sum(packets: List[Packet]) -> int:
    running_sum = 0
    for p in packets:
        if isinstance(p, LiteralPacket):
            running_sum += p.version
        elif isinstance(p, OperatorPacket):
            sub_sum = ver_sum(p.sub_packets)
            running_sum += p.version + sub_sum
    return running_sum


def part_one(in_str: str) -> Tuple[int, List[Packet]]:
    queued_bits = parse_input(in_str.strip())
    packets = bit_list_to_packets(queued_bits)
    return ver_sum(packets), packets


res, packets = part_one("D2FE28")
assert len(packets) == 1
assert isinstance(packets[0], LiteralPacket)
assert packets[0].value == 2021, pprint(packets)

res, packets = part_one("38006F45291200")
assert len(packets) == 1, pprint(packets)
assert isinstance(packets[0], OperatorPacket)
assert packets[0].version == 1
assert packets[0].type_id == 6
assert packets[0].length_type == 0
assert len(packets[0].sub_packets) == 2

res, packets = part_one("8A004A801A8002F478")
assert res == 16, breakpoint()

res, packets = part_one("620080001611562C8802118E34")
assert res == 12, breakpoint()

res, packets = part_one("C0015000016115A2E0802F182340")
assert res == 23, breakpoint()

res, packets = part_one("A0016C880162017C3686B18A3D4780")
assert res == 31, breakpoint()

puzzle_out, _ = part_one(puzzle_input_str)
print(f"Part 1: {puzzle_out}")


def eval_packet(p: Packet):
    if isinstance(p, LiteralPacket):
        return p.value
    elif isinstance(p, OperatorPacket):
        sub_packet_eval = [eval_packet(sub_packet) for sub_packet in p.sub_packets]
        if p.type_id == 0:
            return sum(sub_packet_eval)
        elif p.type_id == 1:
            acc = 1
            results = sub_packet_eval
            for r in results:
                acc *= r
            return acc
        elif p.type_id == 2:
            return min(sub_packet_eval)
        elif p.type_id == 3:
            return max(sub_packet_eval)
        elif p.type_id == 5:
            assert len(sub_packet_eval) == 2
            first, second = sub_packet_eval[0], sub_packet_eval[1]
            return 1 if first > second else 0
        elif p.type_id == 6:
            assert len(p.sub_packets) == 2
            first, second = sub_packet_eval[0], sub_packet_eval[1]
            return 1 if first < second else 0
        elif p.type_id == 7:
            assert len(p.sub_packets) == 2
            first, second = sub_packet_eval[0], sub_packet_eval[1]
            return 1 if first == second else 0
        else:
            raise ValueError("Unexpected type_id")
    else:
        raise ValueError("Unexpected packet type")


def part_two(in_str: str) -> int:
    _, packets = part_one(in_str)
    res = eval_packet(packets[0])
    return res


puzzle_out = part_two(puzzle_input_str)
print(f"Part 2: {puzzle_out}")
