from collections import defaultdict
from typing import Dict, List, TypeVar

from utils import get_input_data, timer
import numpy as np

# Tried doing it with a simple graph search, but that's way too slow
# Don't know about search algorithms, so not gonna bother with this puzzle.

TKey = TypeVar("TKey")
Path = List[TKey]

class Node:
    def __init__(
        self,
        key: TKey,
        neighbors: List[TKey],
        **additional_data
    ) -> None:
        self._key = key
        self._neighbors = neighbors
        self._additional_data = additional_data

    def __repr__(self) -> str:
        return f"<Node {self._key}>"

    @property
    def key(self) -> TKey:
        return self._key

    @property
    def neighbors(self) -> List[TKey]:
        return self._neighbors


class Graph:
    def __init__(self, nodes: List[Node]) -> None:
        self._nodes = nodes
        self._graph: Dict[TKey, Node] = {node.key: node for node in nodes}

    def get_paths_between(
        self,
        start_key: TKey,
        end_key: TKey,
    ) -> List[List[Node]]:
        visited = defaultdict(lambda: False)
        found_paths = []

        self._get_paths_between_recursive(
            start_key,
            end_key,
            visited,
            [],
            found_paths,
        )

        return [
            [self._graph[k] for k in path]
            for path in found_paths
        ]

    def _get_paths_between_recursive(
        self,
        key: TKey,
        end: TKey,
        visited: Dict[TKey, bool],
        path: Path,
        found_path: List[Path],
    ) -> None:
        visited[key] = True
        path.append(key)

        if key == end:
            found_path.append(list(path))
        else:
            for neighbor in self._graph[key].neighbors:
                if not visited[neighbor]:
                    self._get_paths_between_recursive(
                        neighbor, end, visited, path, found_path)

        visited[key] = False
        path.pop(-1)


@timer
def parse_input() -> np.ndarray:
    rows = [
        [int(c) for c in line]
        for line in get_input_data(day=15).splitlines()
    ]

    return np.array(rows, dtype=np.uint8)


if __name__ == "__main__":
    arr = parse_input()
    arr_x_length = np.size(arr, 1)
    arr_y_length = np.size(arr, 0)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    nodes = []
    for x in range(arr_x_length):
        for y in range(arr_y_length):
            neighbors = []
            for dy, dx in directions:
                nx = x + dx
                ny = y + dy
                
                if nx >= 0 and nx < arr_x_length and ny >= 0 and ny < arr_y_length:
                    neighbors.append((ny, nx))

            node = Node(key=(y, x), neighbors=neighbors, value=arr[y, x])
            nodes.append(node)

    print(nodes)
    graph = Graph(nodes=nodes)
    paths = graph.get_paths_between((0, 0), (9, 9))
    print(paths)
