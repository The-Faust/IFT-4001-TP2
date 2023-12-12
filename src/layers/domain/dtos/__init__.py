from typing import Tuple, List


class ShapeGenInputDto(Tuple[List[int], int, List[int], List[int]]):
    pass


class PackingModelInputDto(tuple[int, int, int, List[List[int]], List[List[int]], [{int}], [{int}], [int], [int]]):
    pass
