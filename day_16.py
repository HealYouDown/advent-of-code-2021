from typing import Generator, List, Optional
from utils import get_input_data, timer
import numpy as np


def hex_to_bin(hex_: str) -> str:
    return "".join([bin(int(char, 16))[2:].rjust(4, "0") for char in hex_])


def flatten_packets(packet: "Packet") -> Generator["Packet", None, None]:
    for p in packet.sub_packets:
        if p.has_children:
            yield from flatten_packets(p)
        yield p


class Packet:
    def __init__(self, data_stream: str) -> None:
        self._bits_read = 0

        # Parse the header
        self._version = int(data_stream[:3], 2)
        self._type_id = int(data_stream[3:6], 2)
        self._bits_read += 6

        self._value = None
        self._sub_packets: List[Packet] = []

        # Parse content
        body_stream = data_stream[6:]

        if self._type_id == 4:
            groups = []
            for i in range(0, len(body_stream), 5):
                group = body_stream[i:i+5]
                groups.append(group[1:])

                if group.startswith("0"):
                    break

            self._value = int("".join(groups), 2)
            self._bits_read += len(groups) * 5

        else:  # Sub packets
            length_type_id = int(body_stream[0], 2)
            self._bits_read += 1

            if length_type_id == 0:
                total_length_in_bits = int(body_stream[1:16], 2)
                self._bits_read += 15

                sub_packet_stream = body_stream[16:]
                sub_bits_read = 0
                while sub_bits_read != total_length_in_bits:
                    p = Packet(sub_packet_stream[sub_bits_read:])
                    self._sub_packets.append(p)
                    sub_bits_read += p.bits_read

            elif length_type_id == 1:
                number_of_subpackets = int(body_stream[1:12], 2)
                self._bits_read += 11

                sub_packet_stream = body_stream[12:]
                sub_bits_read = 0
                while len(self._sub_packets) < number_of_subpackets:
                    p = Packet(sub_packet_stream[sub_bits_read:])
                    self._sub_packets.append(p)
                    sub_bits_read += p.bits_read

        self._bits_read += sum(p.bits_read for p in self._sub_packets)

    @property
    def version(self) -> int:
        return self._version

    @property
    def value(self) -> Optional[int]:
        sub_values = [p.value for p in self.sub_packets]

        if self._type_id == 0:
            return sum(sub_values)
        elif self._type_id == 1:
            return np.prod(sub_values)
        elif self._type_id == 2:
            return min(sub_values)
        elif self._type_id == 3:
            return max(sub_values)
        elif self._type_id == 4:
            return self._value
        elif self._type_id == 5:
            return 1 if sub_values[0] > sub_values[1] else 0
        elif self._type_id == 6:
            return 1 if sub_values[0] < sub_values[1] else 0
        elif self._type_id == 7:
            return 1 if sub_values[0] == sub_values[1] else 0

    @property
    def bits_read(self) -> int:
        return self._bits_read

    @property
    def sub_packets(self) -> List["Packet"]:
        return self._sub_packets

    @property
    def has_children(self) -> bool:
        return self._type_id != 4


@timer
def puzzle_1(root_packet: Packet) -> int:
    version_sum = 0

    version_sum += root_packet.version
    for p in flatten_packets(root_packet):
        version_sum += p.version

    return version_sum


@timer
def puzzle_2(root_packet: Packet) -> int:
    return root_packet.value


@timer
def parse_input() -> Packet:
    return Packet(hex_to_bin(get_input_data(day=16)))


if __name__ == "__main__":
    root_packet = parse_input()

    print(puzzle_1(root_packet))
    print(puzzle_2(root_packet))
