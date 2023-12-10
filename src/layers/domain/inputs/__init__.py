from dataclasses import dataclass
from typing import List, Set


@dataclass
class PackingModelInput:
    nObjects: int
    nRectangles: int
    nShapes: int
    rectSize: List[List[int]]
    rectOffset: List[List[int]]
    shape: List[Set[int]]
    validShapes: List[Set[int]]
    l: int
    u: int
