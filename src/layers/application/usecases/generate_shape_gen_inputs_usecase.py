import logging
from typing import Tuple, Iterable
from uuid import uuid4

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_problem_db_service import PackingProblemDbService
from src.layers.domain.dtos import ShapeGenInputDto


class SolvePackingUseCase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_gen_service: DataGenService = DataGenService()
        self.packing_problem_db_service: PackingProblemDbService = PackingProblemDbService()

    def execute(
        self,
        batch_name: str,
        min_bounding_box_limit: Tuple[int, int],
        max_bounding_box_limit: Tuple[int, int],
        n: int = 1,
        write_to_db: bool = False
    ) -> Iterable[ShapeGenInputDto]:
        batch_id = uuid4()
        shape_gen_input_dtos = [
            self.data_gen_service\
                .randomly_generate_shape_model_input(min_bounding_box_limit, max_bounding_box_limit) for _ in range(n)
        ]

        self.logger.debug(shape_gen_input_dtos)

        shape_gen_input_rows = self.packing_problem_db_service.write_shape_gen_model_inputs_to_table(
            batch_name=batch_name,
            batch_id=batch_id,
            shape_gen_input_dtos=shape_gen_input_dtos,
            write_to_db=write_to_db
        )

        self.logger.debug(shape_gen_input_rows)

        packing_model_inputs = [
            (row['batch_name'], row['batch_id'], row['input_id'],
             self.data_gen_service.generate_packing_model_inputs(row['inputs']))
            for row in shape_gen_input_rows
        ]

        self.logger.debug(f'---------------------------------------------------{packing_model_inputs}')

        return []
