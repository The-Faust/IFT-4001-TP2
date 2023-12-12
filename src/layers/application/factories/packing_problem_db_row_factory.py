import logging
from datetime import datetime
from typing import Iterable, Dict
from uuid import uuid4

from src.layers.domain.dtos import ShapeGenInputDto
from src.layers.domain.inputs import PackingModelInput
from src.layers.domain.solutions import PackingModelSolution
from src.layers.domain.tables.packing_problem.packing_model_input_table import PackingModelInputTable
from src.layers.domain.tables.packing_problem.packing_model_solution_table import PackingModelSolutionTable
from src.layers.domain.tables.packing_problem.shape_gen_model_input_table import ShapeGenModelInputTable


class PackingProblemDbRowFactory:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def make_packing_model_solution_row(
        self,
        batch_name: str,
        batch_id: uuid4,
        packing_model_input_id: uuid4,
        packing_model_solution: PackingModelSolution
    ) -> Iterable[PackingModelSolutionTable]:
        return [PackingModelSolutionTable(
            batch_name=batch_name,
            batch_id=batch_id,
            packing_model_input_id=packing_model_input_id,
            input_id=uuid4(),
            inputs=packing_model_solution.__dict__,
            generation_time=datetime.now()
        )]

    def convert_packing_model_input_rows_to_dataclass(self, packing_model_input_row: Dict[str, any]) -> Dict[str, any]:
        packing_model_input = packing_model_input_row['inputs']
        packing_model_input['shape'] = [set(s) for s in packing_model_input['shape']]
        packing_model_input['validShapes'] = [set(vs) for vs in packing_model_input['validShapes']]

        packing_model_input_row['inputs'] = PackingModelInput(**packing_model_input)

        return packing_model_input_row

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
        arguments_to_modify = ['shape', 'validShapes']

        inputs = {k: v for k, v in packing_model_input.__dict__.items() if k not in arguments_to_modify}
        inputs = {
            'shape': [list(s) for s in packing_model_input.shape],
            'validShapes': [list(vs) for vs in packing_model_input.validShapes],
            **inputs
        }

        row_arguments = dict(
            batch_name=batch_name,
            batch_id=batch_id,
            shape_gen_input_id=shape_gen_input_id,
            input_id=uuid4(),
            inputs=inputs,
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
