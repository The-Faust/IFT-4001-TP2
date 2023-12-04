import logging
from datetime import timedelta
from pathlib import Path
from typing import Tuple, Union, List

from minizinc import Solver, Instance, Result
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
        min_bounding_box_limits: Tuple[int, int] = (1, 1),
        max_bounding_box_limits: Tuple[int, int] = (5, 5),
        timeout: int = 600,
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

        (bounding_box, n_shapes, surface_per_shapes, rectangles_count_per_shape) = self \
            .randomly_generate_shape_model_input(min_bounding_box_limits, max_bounding_box_limits)

        self.logger.debug(
            f'bounding_box={bounding_box}\n'
            f'n_shapes={n_shapes}\n'
            f'surface_per_shapes={surface_per_shapes}\n'
            f'rectangles_count_per_shape={rectangles_count_per_shape}'
        )

        instance = Instance(solver, model)
        instance["boundingBox"] = bounding_box  # [4, 3]
        instance["nShapes"] = n_shapes  # 4
        instance["surfacePerShape"] = surface_per_shapes  # [3, 4, 1, 2]
        instance["rectanglesCountPerShape"] = rectangles_count_per_shape  # [2, 2, 1, 1]

        solution = instance.solve(timeout=timedelta(timeout), free_search=True)
        #self.logger.debug(solution)

        (n_objects,n_rect,n_shapes,rect_size,rect_offset,shape,valid_shapes,l,u) = self \
            .solution_to_packing_data(instance, solution)

        data = {
            "nObjects": n_objects,
            "nRectangles": n_rect,
            "nShapes": n_shapes,
            "rectSize": rect_size,
            "rectOffset": rect_offset,
            "shape": shape,
            "validShapes": valid_shapes,
            "l": l,
            "u": u
        }
        return data

    def randomly_generate_shape_model_input(
        self,
        min_bounding_box_limits: Tuple[int, int] = (1, 1),
        max_bounding_box_limits: Tuple[int, int] = (5, 5)
    ) -> Tuple[List[int], int, List[int], List[int]]:
        """

        Args:
            bounding_box_limits: generate randomly
            min_bounding_box_limits:
            surface_per_shape:
            rectangles_count_per_shape:
            files:

        Returns:

        """
        bounding_box: List[int] = list([
            randint(min_bounding_box_limits[0], max_bounding_box_limits[0]),
            randint(min_bounding_box_limits[1], max_bounding_box_limits[1])
        ])

        n_shape: int = randint(1, (bounding_box[0] * bounding_box[1])+1)

        surface_per_shape: List[int] = list([
            (randint(1, bounding_box[0]) if 1 < bounding_box[0] else 1)
            * (randint(1, bounding_box[1]) if 1 < bounding_box[1] else 1)
            for _ in range(n_shape)
        ])

        rectangles_count_per_shape: List[int] = list([
            randint(1, surface_per_shape[i])
            if 1 < surface_per_shape[i] else 1
            for i in range(n_shape)
        ])

        return bounding_box, n_shape, surface_per_shape, rectangles_count_per_shape

    def solution_to_packing_data(self, instance: Instance,solution: Result)\
            ->tuple[int,int,int,List[List[int]],List[List[int]],[{int}],[{int}],[int],[int]]:
        n_objects: int = instance["nShapes"]
        n_rect: int = solution["rectanglesCount"]
        rectangles_count_per_shape: List[int] = instance["rectanglesCountPerShape"]
        n_shapes: int = n_objects
        rect_size: List[List[int, int]] = solution["rect_size"][:n_rect]
        rect_offset: List[List[int, int]] = solution["real_rect_offset"][:n_rect]
        shape: [{int}] = [set(solution["shape"][i][:rectangles_count_per_shape[i]]) for i in range(n_objects)]
        valid_shapes: [{int}] = [{i+1} for i in range(n_objects)]

        return n_objects,n_rect,n_shapes,rect_size,rect_offset,shape,valid_shapes,[0,0],[4, 4]

    # def rotate_shapes(self,  shape: List[List[int]], rect_size: List[List[int, int]]):
    #     for i in range(len(shape)):
    #         if len(shape[i]) > 1:
    #             pass
    #         else:
    #             if rect_size[shape[i][0],0] > rect_size[shape[i][0],1]:
    #                 pass
    #             elif rect_size[shape[i][0],0] < rect_size[shape[i][0],1]:
    #                 pass
