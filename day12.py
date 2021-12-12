from typing import Dict, List, Tuple
from utils import get_input_data, timer
from collections import defaultdict

CAVE_GRAPH = Dict[str, List[str]]


def find_paths_p1(
    graph: CAVE_GRAPH,
    root_node: str,
    current_path: List[str],
    finished_paths: List[Tuple[str]]
) -> List[Tuple[str]]:
    current_path.append(root_node)

    for child_node in graph[root_node]:
        if child_node == "start":
            continue

        if child_node in current_path and not child_node.isupper():
            continue

        if child_node == "end":
            finished_paths.append(tuple([*current_path, "end"]))
            continue

        for child in find_paths_p1(graph, child_node, list(current_path), []):
            if child[-1] == "end":
                finished_paths.append(tuple(child))

    return finished_paths


@timer
def puzzle_1(graph: CAVE_GRAPH) -> int:
    return len(find_paths_p1(graph, "start", [], []))
 

@timer
def puzzle_2(graph: CAVE_GRAPH):
    pass
    # Using if any(current_path.count(char) >= 2 for char in current_path if char.islower() and char != "start"): continue
    # to only allow one path with two smaller caves does not work and I'm out of ideas, except maybe bruteforcing
    # all possible paths and validating them to match the requirements, but that's ugly.


@timer
def parse_input() -> CAVE_GRAPH:
    connections = defaultdict(list)
    for line in get_input_data(day=12).splitlines():
        a, b = line.split("-")
        connections[a].append(b)
        connections[b].append(a)

    return connections


if __name__ == "__main__":
    graph = parse_input()

    print(puzzle_1(graph))
    print(puzzle_2(graph))
