import logging
from typing import Iterable, Tuple

from numpy.random import randint, choice


class DataGenService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate(self, n_shapes: int = 10, max_number_of_parts: int = 2):
        valid_shapes = self.generate_valid_shapes(n_shapes)

        self.logger.debug(f'valid shapes are:\n    {tuple(valid_shapes)}')

        shapes = self.generate_shapes(valid_shapes, max_number_of_parts)

        self.logger.debug(f'shapes are:\n    {tuple(shapes)}')

        return

    def generate_valid_shapes(self, n_shapes: int) -> Iterable[Tuple[int, ...]]:
        shape_lengths = [choice([1, 2, 4]) for _ in range(n_shapes)]

        i = 1

        for shape_length in shape_lengths:
            yield tuple(i + j for j in range(shape_length))

            i += shape_length

    def generate_shapes(self, valid_shapes: Iterable[Tuple[int, ...]], max_number_of_parts: int) -> Iterable[Tuple[int]]:
        return (self.generate_shape(valid_shape, max_number_of_parts) for valid_shape in valid_shapes)

    def generate_shape(
        self,
        valid_shape: Tuple[int, ...],
        max_number_of_parts: int = 2
    ) -> Tuple[int, ...]:
        len_shape = len(valid_shape)
        number_of_parts = randint(1, max_number_of_parts)

        i = 1

        if len_shape == 4:
            shape = []

            for i in valid_shape:
                pass

        elif len_shape == 2:
            shape = []
            pass

        else:
            shape = (*valid_shape, )

        return shape

    def generate_offset(
        self,
        max_size: int,
        rectangles: Iterable[Tuple[int, int]]
    ) -> Iterable[Tuple[int, int]]:
        pass

    def generate_rectangles(self, max_size: int, n: int) -> Iterable[Tuple[int, int]]:
        return ((randint(1, max_size), randint(1, max_size)) for _ in range(n))
