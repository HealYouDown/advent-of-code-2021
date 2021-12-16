from typing import List, Optional
from utils import get_input_data, timer


def hex_to_bin(hex_: str) -> str:
    return "".join([bin(int(char, 16))[2:].rjust(4, "0") for char in hex_])


def flatten(container: list):
    for item in container:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


class Packet:
    def __init__(self, data_stream: str) -> None:
        self._bits_read = 0
        self._bits_read_padded = 0

        # Parse the header
        self._version = int(data_stream[:3], 2)
        self._type_id = int(data_stream[3:6], 2)
        self._bits_read += 6

        self._value = None
        self._sub_packets: List[Packet] = []
        self._last_stream_index = 0

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
        return self._value

    @property
    def bits_read(self) -> int:
        return self._bits_read

    @property
    def sub_packets(self) -> List["Packet"]:
        return self._sub_packets


@timer
def puzzle_1(bit_stream: str) -> int:
    root_packet = Packet(bit_stream)
    version_sum = 0

    version_sum += root_packet.version
    for p in flatten(root_packet.sub_packets)
        version_sum += 

@timer
def parse_input() -> str:
    return hex_to_bin(get_input_data(day=16))


if __name__ == "__main__":
    bit_stream = parse_input()

    print(puzzle_1(bit_stream))
