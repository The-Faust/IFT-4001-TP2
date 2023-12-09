import logging
from typing import Dict, Union, Iterable
from uuid import uuid4

from src.layers.domain.dtos import ShapeGenInputDto
from src.layers.domain.inputs import PackingModelInput
from src.layers.domain.tables.packing_problem.packing_model_input_table import PackingModelInputTable
from src.layers.domain.tables.packing_problem.shape_gen_model_input_table import ShapeGenModelInputTable


class PackingProblemDbRowFactory:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def make_packing_model_input_rows(
        self,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_inputs: Iterable[PackingModelInput]
    ) -> Iterable[Dict[str: Union[uuid4, Dict[str, Union[int, Iterable[any]]]]]]:
        return (
            self.make_packing_model_input_row(batch_id, shape_gen_input_id, packing_model_input)
            for packing_model_input in packing_model_inputs
        )

    def make_packing_model_input_row(
        self,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_input: PackingModelInput
    ):
        row_arguments = dict(
            batch_id=batch_id,
            shape_gen_input_id=shape_gen_input_id,
            input_id=uuid4(),
            inputs=packing_model_input.__dict__
        )

        return PackingModelInputTable(**row_arguments)

    def make_shape_gen_input_rows(
        self,
        batch_id: uuid4,
        shape_gen_input_dtos: Iterable[ShapeGenInputDto]
    ) -> Iterable[Dict[str: Union[uuid4, Dict[str, Union[int, Iterable[any]]]]]]:
        self.logger.debug('calling method make_shape_gen_input_rows')

        return (
            self.make_shape_gen_input_row(batch_id, shape_gen_input_dto)
            for shape_gen_input_dto in shape_gen_input_dtos
        )


    def make_shape_gen_input_row(
        self,
        batch_id: uuid4,
        shape_gen_input_object: ShapeGenInputDto
    ) -> Dict[str: Union[uuid4, Dict[str, Union[int, Iterable]]]]:
        self.logger.debug('calling method make_shape_gen_input_row')

        (bounding_box, n_shapes, surface_per_shapes, rectangles_count_per_shape) = shape_gen_input_object
        inputs = dict(
            bounding_box=bounding_box,
            n_shapes=n_shapes,
            surface_per_shapes=surface_per_shapes,
            rectangles_count_per_shape=rectangles_count_per_shape
        )

        row_arguments = dict(
            batch_id=batch_id,
            input_id=uuid4(),
            inputs=inputs
        )

        self.logger.debug(row_arguments)

        return ShapeGenModelInputTable(**row_arguments)
