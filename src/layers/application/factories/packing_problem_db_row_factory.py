import logging
from datetime import datetime
from typing import Iterable
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
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_inputs: Iterable[PackingModelInput]
    ) -> Iterable[PackingModelInputTable]:
        return (
            self.make_packing_model_input_row(batch_name, batch_id, shape_gen_input_id, packing_model_input)
            for packing_model_input in packing_model_inputs
        )

    def make_packing_model_input_row(
        self,
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_input: PackingModelInput
    ) -> PackingModelInputTable:
        row_arguments = dict(
            batch_name=batch_name,
            batch_id=batch_id,
            shape_gen_input_id=shape_gen_input_id,
            input_id=uuid4(),
            inputs=packing_model_input.__dict__,
            generation_time=datetime.now()
        )

        return PackingModelInputTable(**row_arguments)

    def make_shape_gen_input_rows(
        self,
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_dtos: Iterable[ShapeGenInputDto]
    ) -> Iterable[ShapeGenModelInputTable]:
        self.logger.debug('calling method make_shape_gen_input_rows')

        return (
            self.make_shape_gen_input_row(batch_name, batch_id, shape_gen_input_dto)
            for shape_gen_input_dto in shape_gen_input_dtos
        )


    def make_shape_gen_input_row(
        self,
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_object: ShapeGenInputDto
    ) -> ShapeGenModelInputTable:
        self.logger.debug('calling method make_shape_gen_input_row')

        (bounding_box, n_shapes, surface_per_shapes, rectangles_count_per_shape) = shape_gen_input_object
        inputs = dict(
            bounding_box=bounding_box,
            n_shapes=n_shapes,
            surface_per_shapes=surface_per_shapes,
            rectangles_count_per_shape=rectangles_count_per_shape
        )

        row_arguments = dict(
            batch_name=batch_name,
            batch_id=batch_id,
            input_id=uuid4(),
            inputs=inputs,
            generation_time=datetime.now()
        )

        self.logger.debug(row_arguments)

        return ShapeGenModelInputTable(**row_arguments)
