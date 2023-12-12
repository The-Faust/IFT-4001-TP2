from dataclasses import dataclass
from typing import List


@dataclass
class PackingModelSolution:
    objective: int
    x: List[int]
    kind: List[int]
    chosen_objects: List[int]
    chosen_objects_count: int
    surface: int
