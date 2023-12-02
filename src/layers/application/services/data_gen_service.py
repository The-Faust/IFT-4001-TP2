import logging
from datetime import timedelta
from pathlib import Path
from typing import Tuple, Union

from minizinc import Solver, Instance
from numpy.random import randint

from src.layers.application.factories.shape_gen_model_factory import ShapeGenModelFactory


class DataGenService:
    """
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.shape_gen_model_factory: ShapeGenModelFactory = ShapeGenModelFactory()

    def generate(
        self,
        solver: str = 'chuffed',
        min_bounding_box_limits: Tuple[int, int] = (5, 5),
        max_bounding_box_limits: Tuple[int, int] = (10, 10),
        timeout: int = 300,
        files: Union[str, Path] = None
    ) -> any:
        """

        Args:
            solver:
            min_bounding_box_limits:
            max_bounding_box_limits:
            timeout:
            files:

        Returns:

        """
        solver = Solver.lookup(solver)
        model = self.shape_gen_model_factory.make_data_gen_model(files)

        (bounding_box, dimension, n_shapes, surface_per_shapes, rectangles_count_per_shape) = self \
            .randomly_generate_shape_model_input(min_bounding_box_limits, max_bounding_box_limits)
        self.logger.debug(f'bounding_box={bounding_box}\n'
                          f'dimension={dimension}\n'
                          f'n_shapes={n_shapes}\n'
                          f'surface_per_shapes={surface_per_shapes}\n'
                          f'rectangles_count_per_shape={rectangles_count_per_shape}'
                          )

        instance = Instance(solver, model)
        instance['boundingBox'] = bounding_box,
        instance['dimensions'] = dimension
        instance['nShapes'] = n_shapes
        instance['surfacePerShape'] = surface_per_shapes
        instance['rectanglesCountPerShape'] = rectangles_count_per_shape

        solution = instance.solve(timeout=timedelta(timeout), free_search=True)

        self.logger.debug(solution)

        return solution

    def randomly_generate_shape_model_input(
        self,
        min_bounding_box_limits: Tuple[int, int] = (5, 5),
        max_bounding_box_limits: Tuple[int, int] = (10, 10)
    ) -> Tuple[Tuple[int, int], int, int, Tuple[int, ...], Tuple[int, ...]]:
        """

        Args:
            bounding_box_limits: generate randomly
            min_bounding_box_limits:
            surface_per_shape:
            rectangles_count_per_shape:
            files:

        Returns:

        """
        bounding_box: Tuple[int, int] = (
            randint(min_bounding_box_limits[0], max_bounding_box_limits[0]),
            randint(min_bounding_box_limits[1], max_bounding_box_limits[1])
        )

        n_shape: int = randint(1, bounding_box[0] * bounding_box[1])

        surface_per_shape: Tuple[int, ...] = tuple(
            randint(1, bounding_box[0]) * randint(1, bounding_box[1])
            for _ in range(n_shape)
        )

        rectangles_count_per_shape: Tuple[int, ...] = tuple(randint(1, surface_per_shape[i]) for i in range(n_shape))

        return bounding_box, 2, n_shape, surface_per_shape, rectangles_count_per_shape
