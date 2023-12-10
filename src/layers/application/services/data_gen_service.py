import logging
import math
import random
from datetime import timedelta
from pathlib import Path
from typing import Tuple, Union, List, Set, Dict, Iterable
from uuid import uuid4

from minizinc import Solver, Instance, Result
from numpy.random import randint

from src.layers.application.factories.shape_factory import ShapeFactory
from src.layers.application.factories.shape_gen_model_factory import ShapeGenModelFactory
from src.layers.domain.dtos import ShapeGenInputDto, PackingModelInputDto
from src.layers.domain.inputs import PackingModelInput


class DataGenService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.shape_gen_model_factory: ShapeGenModelFactory = ShapeGenModelFactory()
        self.shape_factory: ShapeFactory = ShapeFactory()

    def generate_packing_model_inputs(
        self,
        shape_gen_model_input: Dict[str, any],
        solver: str = 'chuffed',
        timeout: int = 600,
        files: Union[str, Path] = None
    ) -> PackingModelInput:
        solver = Solver.lookup(solver)
        model = self.shape_gen_model_factory.make_data_gen_model(files)

        self.logger.debug(shape_gen_model_input)

        bounding_box = shape_gen_model_input['bounding_box']
        n_shapes = shape_gen_model_input['n_shapes']
        surface_per_shapes = shape_gen_model_input['surface_per_shapes']
        rectangles_count_per_shape = shape_gen_model_input['rectangles_count_per_shape']

        self.logger.debug(
            f'bounding_box={bounding_box}\n'
            f'n_shapes={n_shapes}\n'
            f'surface_per_shapes={surface_per_shapes}\n'
            f'rectangles_count_per_shape={rectangles_count_per_shape}'
        )

        instance = Instance(solver, model)
        instance["boundingBox"] = bounding_box
        instance["nShapes"] = n_shapes
        instance["surfacePerShape"] = surface_per_shapes
        instance["rectanglesCountPerShape"] = rectangles_count_per_shape

        solution = instance.solve(timeout=timedelta(timeout), free_search=True)

        (n_objects, n_rect, n_shapes, rect_size, rect_offset, shape, valid_shapes, l, u) = self \
            .produce_packing_model_input(instance, solution)

        packing_model_input = PackingModelInput(
            nObjects=n_objects,
            nRectangles=n_rect,
            nShapes=n_shapes,
            rectSize=rect_size,
            rectOffset=rect_offset,
            shape=shape,
            validShapes=valid_shapes,
            l=l, u=u
        )

        self.logger.debug(packing_model_input)

        return packing_model_input

    def randomly_generate_shape_model_input(
        self,
        min_bounding_box_limits: Tuple[int, int],
        max_bounding_box_limits: Tuple[int, int],
    ) -> ShapeGenInputDto:
        bounding_box: List[int] = list([
            randint(min_bounding_box_limits[0], max_bounding_box_limits[0]),
            randint(min_bounding_box_limits[1], max_bounding_box_limits[1])
        ])

        shape_ratio: int = math.ceil((bounding_box[0] * bounding_box[1]) / 10)

        n_shape: int = 10 + shape_ratio

        surface_per_shape: List[int] = list([
            max(1, min(int(random.gauss(max(1, shape_ratio), shape_ratio)),
                       max(1, bounding_box[0] * bounding_box[1])))
            for _ in range(n_shape)
        ])

        rectangles_count_per_shape: List[int] = list([
            randint(1, surface_per_shape[i])
            if 1 < surface_per_shape[i] else 1
            for i in range(n_shape)
        ])

        shape_gen_dto = ShapeGenInputDto([
            bounding_box,
            n_shape,
            surface_per_shape,
            rectangles_count_per_shape
        ])

        self.logger.debug(shape_gen_dto)

        return shape_gen_dto

    def produce_packing_model_input(
        self,
        instance: Instance,
        solution: Result
    ) -> PackingModelInputDto:
        n_objects: int = instance["nShapes"]
        n_rect: int = solution["rectanglesCount"]
        rectangles_count_per_shape: List[int] = instance["rectanglesCountPerShape"]
        rect_size: List[List[int]] = solution["rect_size"][:n_rect]
        rect_offset: List[List[int, int]] = solution["real_rect_offset"][:n_rect]
        shape: List[Set[int]] = [set(solution["shape"][i][:rectangles_count_per_shape[i]]) for i in range(n_objects)]
        valid_shapes: [{int}] = [{i + 1} for i in range(n_objects)]

        self.shape_factory.remove_duplicates(rect_size, rect_offset, shape, valid_shapes)
        self.shape_factory.rotate_shapes(shape, rect_size, rect_offset, valid_shapes)

        # on ajoute la shape vide
        rect_size.append([0, 0])
        rect_offset.append([0, 0])
        n_rect = len(rect_size)
        shape.append({n_rect})
        n_shapes: int = len(shape)
        valid_shapes.append({n_shapes})
        n_objects += 1

        # sort valid shapes de la plus grande surface a la plus petite
        valid_shapes.sort(key=lambda x: sum(
            rect_size[list(shape[list(x)[0] - 1])[i] - 1][0] * rect_size[list(shape[list(x)[0] - 1])[i] - 1][1]
            for i in range(len(shape[list(x)[0] - 1]))), reverse=True)

        return PackingModelInputDto([
            n_objects, n_rect, n_shapes,
            rect_size, rect_offset, shape,
            valid_shapes, [0, 0],
            [instance["boundingBox"][0], instance["boundingBox"][1]]]
        )
