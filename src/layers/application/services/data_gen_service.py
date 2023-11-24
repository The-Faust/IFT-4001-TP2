import logging
from typing import Iterable, Tuple


class DataGenService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_rectangles(self, max_size: int):
        pass

    def generate_offset(
            self,
            max_size: int,
            rectangles: Iterable[Tuple[int, int]]
    ) -> Iterable[Tuple[int, int]]:
        pass

    def generate_shape(
            self,
            rectangles: Iterable[Tuple[int, int]],
            offsets: Iterable[Tuple[int, int]]
    ) -> Iterable[Tuple[int, ...]]:
        pass

    def generate_valid_shapes(
            self,
            rectangles: Iterable[Tuple[int, int]],
            offsets: Iterable[Tuple[int, int]],
            shapes: Iterable[Tuple[int, ...]]
    ) -> Iterable[Tuple[int, ...]]:
        pass
