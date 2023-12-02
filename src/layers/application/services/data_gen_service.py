import logging
from pathlib import Path
from typing import Tuple, Union

from src.layers.application.factories.shape_gen_model_factory import ShapeGenModelFactory


class DataGenService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.shape_gen_model_factory: ShapeGenModelFactory = ShapeGenModelFactory()

    def generate(self, n_shapes: int = 10, max_number_of_parts: int = 2):
        valid_shapes = self.generate_valid_shapes(n_shapes)

        self.logger.debug(f'valid shapes are:\n    {tuple(valid_shapes)}')

        shapes = self.generate_shapes(valid_shapes, max_number_of_parts)

        self.logger.debug(f'shapes are:\n    {tuple(shapes)}')

        return

    def generate_bounds(
        self,
        bounding_box_limits: Tuple[int, int],
        dimensions: int,
        surface_per_shape: Tuple[int, ...],
        rectangles_count_per_shape: Tuple[int, ...],
        files: Union[str, Path] = None
    ):
        self.shape_gen_model_factory.make_data_gen_model(files)

