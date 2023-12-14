import logging
from typing import Tuple, Iterable
from uuid import uuid4

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_problem_db_service import PackingProblemDbService
from src.layers.application.services.packing_service import PackingService
from src.layers.domain.dtos import ShapeGenInputDto


class SolvePackingUseCase:
    """
    Normalement on ferait tout ceci en plusieurs appels, mais nos contraintes de temps nous forces à procéder ainsi
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_gen_service: DataGenService = DataGenService()
        self.packing_problem_db_service: PackingProblemDbService = PackingProblemDbService()
        self.packing_service: PackingService = PackingService()

    def execute(
        self,
        batch_name: str,
        min_bounding_box_limit: Tuple[int, int],
        max_bounding_box_limit: Tuple[int, int],
        n: int = 1,
        write_to_db: bool = False
    ) -> Iterable[any]:
        batch_id = uuid4()
        shape_gen_input_dtos = [
            self.data_gen_service \
                .randomly_generate_shape_model_input(min_bounding_box_limit, max_bounding_box_limit) for _ in range(n)
        ]

        #self.logger.debug(shape_gen_input_dtos)

        shape_gen_input_rows = self.packing_problem_db_service.write_shape_gen_model_inputs_to_table(
            batch_name=batch_name,
            batch_id=batch_id,
            shape_gen_input_dtos=shape_gen_input_dtos,
            write_to_db=write_to_db
        )

        self.logger.debug(shape_gen_input_rows)

        packing_model_inputs = [
            (row['input_id'], self.data_gen_service.generate_packing_model_inputs(row['inputs']))
            for row in shape_gen_input_rows
        ]

        self.logger.debug(packing_model_inputs)

        packing_model_input_rows = [
            self.packing_problem_db_service.write_packing_model_inputs_to_table(
                batch_name=batch_name,
                batch_id=batch_id,
                shape_gen_input_id=shape_gen_input_id,
                packing_model_inputs=[packing_model_input],
                write_to_db=write_to_db
            ) for shape_gen_input_id, packing_model_input in packing_model_inputs
        ]
        #  flatten them inputs
        packing_model_input_rows = [row for shape_gen_row in packing_model_input_rows for row in shape_gen_row]

        packing_solutions = [
            (row['input_id'], self.packing_service.solve(row['inputs']))
            for row in packing_model_input_rows
        ]

        # for packing_solution in packing_solutions:
        #     self.logger.debug(packing_solution)

        packing_solution_rows = [
            self.packing_problem_db_service.write_packing_model_solution_to_table(
                batch_name=batch_name,
                batch_id=batch_id,
                packing_model_input_id=packing_model_input_id,
                packing_model_solution=packing_model_solution,
                write_to_db=write_to_db
            )
            for (packing_model_input_id, packing_model_solution) in packing_solutions
        ]
        packing_solution_rows = [row for input in packing_solution_rows for row in input]

        self.logger.debug(packing_solution_rows)

        return packing_model_input_rows, packing_solution_rows
