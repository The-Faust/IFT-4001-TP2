import logging
import math
import random
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
            min_bounding_box_limits: Tuple[int, int] = (4, 4),
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

        (n_objects, n_rect, n_shapes, rect_size, rect_offset, shape, valid_shapes, l, u) = self \
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
            min_bounding_box_limits: Tuple[int, int],
            max_bounding_box_limits: Tuple[int, int]
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

        shape_ratio: int = math.ceil((bounding_box[0] * bounding_box[1]) / 10)

        n_shape: int = 10 + shape_ratio#math.floor((bounding_box[0] * bounding_box[1])/2)#randint(1, (bounding_box[0] * bounding_box[1]) + 1)

        surface_per_shape: List[int] = list([
            max(1, min(int(random.gauss(max(1,shape_ratio),shape_ratio)),
                       max(1,bounding_box[0] * bounding_box[1])))
            for _ in range(n_shape)
        ])


        rectangles_count_per_shape: List[int] = list([
            randint(1, surface_per_shape[i])
            if 1 < surface_per_shape[i] else 1
            for i in range(n_shape)
        ])

        return bounding_box, n_shape, surface_per_shape, rectangles_count_per_shape

    def solution_to_packing_data(self, instance: Instance, solution: Result) \
            -> tuple[int, int, int, List[List[int]], List[List[int]], [{int}], [{int}], [int], [int]]:
        n_objects: int = instance["nShapes"]
        n_rect: int = solution["rectanglesCount"]
        rectangles_count_per_shape: List[int] = instance["rectanglesCountPerShape"]
        rect_size: List[List[int, int]] = solution["rect_size"][:n_rect]
        rect_offset: List[List[int, int]] = solution["real_rect_offset"][:n_rect]
        shape: [{int}] = [set(solution["shape"][i][:rectangles_count_per_shape[i]]) for i in range(n_objects)]
        valid_shapes: [{int}] = [{i + 1} for i in range(n_objects)]

        self.remove_duplicates(rect_size,rect_offset,shape,valid_shapes)

        self.rotate_shapes(shape, rect_size, rect_offset, valid_shapes)

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
            rect_size[list(shape[list(x)[0]-1])[i] - 1][0] * rect_size[list(shape[list(x)[0]-1])[i] - 1][1]
            for i in range(len(shape[list(x)[0]-1]))),reverse=True)

        return n_objects, n_rect, n_shapes, rect_size, rect_offset, shape, valid_shapes, [0, 0], [
            instance["boundingBox"][0], instance["boundingBox"][1]]

    def remove_duplicates(self,rect_size: List[List[int]],rect_offset: List[List[int]], shape: [{int}],valid_shapes: [{int}]):

        for i in range(len(shape)):
            shape[i] = list(shape[i])

        rect_to_delete:List[int] = []
        for i in range(len(rect_size)-1):
            for j in range(i + 1, len(rect_size)):
                if i not in rect_to_delete and j not in rect_to_delete:
                    if rect_size[i] == rect_size[j] and rect_offset[i] == rect_offset[j]:
                        rect_to_delete.append(j)
                        for k in range(len(shape)):
                            for l in range(len(shape[k])):
                                if list(shape[k])[l] == j + 1:
                                    shape[k][l] = i + 1


        rect_to_delete.sort(reverse=True)
        for i in rect_to_delete:
            for j in range(len(shape)):
                for k in range(len(shape[j])):
                    if list(shape[j])[k] > i+1:
                        shape[j][k] -=1

            rect_size.pop(i)
            rect_offset.pop(i)

        for i in range(len(shape)):
            shape[i] = set(shape[i])

        for i in range(len(valid_shapes)):
            valid_shapes[i] = list(valid_shapes[i])

        shape_to_delete: List[int] = []
        for i in range(len(shape)-1):
            for j in range(i + 1, len(shape)):
                if i not in shape_to_delete and j not in shape_to_delete:
                    if shape[i] == shape[j]:
                        shape_to_delete.append(j)
                        for k in range(len(valid_shapes)):
                            for l in range(len(valid_shapes[k])):
                                if list(valid_shapes[k])[l] == j + 1:
                                    valid_shapes[k][l] = i + 1

        shape_to_delete.sort(reverse=True)
        for i in shape_to_delete:
            for j in range(len(valid_shapes)):
                for k in range(len(valid_shapes[j])):
                    if list(valid_shapes[j])[k] > i+1:
                        valid_shapes[j][k] -=1

            shape.pop(i)

        for i in range(len(valid_shapes)):
            valid_shapes[i] = set(valid_shapes[i])
    def rotate_shapes(self, shape: [{int}], rect_size: List[List[int]], rect_offset: List[List[int]],
                      valid_shapes: [{int}]):
        initial_len: int = len(shape)
        for i in range(initial_len):

            if len(shape[i]) > 1:
                # ordre -> sens horaire
                x_max: int = rect_size[list(shape[i])[0] - 1][0] + rect_offset[list(shape[i])[0] - 1][0]
                y_max: int = rect_size[list(shape[i])[0] - 1][1] + rect_offset[list(shape[i])[0] - 1][1]
                new_shape: [{int}] = [set(), set(), set()]

                for j in range(1, len(shape[i])):
                    x: int = rect_size[list(shape[i])[j] - 1][0] + rect_offset[list(shape[i])[j] - 1][0]
                    y: int = rect_size[list(shape[i])[j] - 1][1] + rect_offset[list(shape[i])[j] - 1][1]
                    if x > x_max: x_max = x
                    if y > y_max: y_max = y
                for j in range(len(shape[i])):
                    current_rect: int = list(shape[i])[j] - 1
                    inverted_x: int = x_max - (rect_offset[current_rect][0] + rect_size[current_rect][0])
                    inverted_y: int = y_max - (rect_offset[current_rect][1] + rect_size[current_rect][1])

                    # rot1
                    new_shape[0].add(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [rect_offset[current_rect][1], inverted_x], rect_size,
                                                        rect_offset))

                    # rot2
                    new_shape[1].add(self.add_rectangle(rect_size[current_rect],
                                                        [inverted_x, inverted_y], rect_size, rect_offset))

                    # rot3
                    new_shape[2].add(self.add_rectangle([rect_size[current_rect][1], rect_size[current_rect][0]],
                                                        [inverted_y, rect_offset[current_rect][0]], rect_size,
                                                        rect_offset))

                for j in range(3): valid_shapes[i].add(self.add_shape(shape, new_shape[j]))



            elif rect_size[list(shape[i])[0] - 1][1] != rect_size[list(shape[i])[0] - 1][0]:
                valid_shapes[i].add(self.add_shape(shape, {
                    self.add_rectangle([rect_size[list(shape[i])[0] - 1][1], rect_size[list(shape[i])[0] - 1][0]],
                                       [0, 0], rect_size, rect_offset, True)}))

    def add_rectangle(self, size: List[int], offset: List[int], rect_size: List[List[int]],
                      rect_offset: List[List[int]],
                      size_only: bool = False) \
            -> int:
        if size_only:
            for i in range(len(rect_size)):
                if rect_size[i] == size: return i + 1
        else:
            for i in range(len(rect_size)):
                if rect_size[i] == size and rect_offset[i] == offset: return i + 1

        rect_size.append(size)
        rect_offset.append(offset)
        return len(rect_size)

    def add_shape(self, shape: [{int}], new_shape: {int}) \
            -> int:
        for i in range(len(shape)):
            if shape[i] == new_shape: return i + 1

        shape.append(new_shape)
        return len(shape)
