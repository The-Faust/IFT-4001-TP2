from typing import Tuple, Iterable, List
from uuid import uuid4

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_problem_db_service import PackingProblemDbService
from src.layers.domain.dtos import ShapeGenInputDto


class GenerateShapeGenInputsUseCase:
    def __init__(self):
        self.data_gen_service: DataGenService = DataGenService()
        self.packing_problem_db_service: PackingProblemDbService = PackingProblemDbService()

    def execute(
        self,
        min_bounding_box_limit: Tuple[int, int],
        max_bounding_box_limit: Tuple[int, int],
        n: int = 1,
        write_to_db: bool = False
    ) -> Iterable[ShapeGenInputDto]:
        batch_id = uuid4()
        inputs = [-1]

        for _ in range(n):
            self.data_gen_service\
                .randomly_generate_shape_model_input(min_bounding_box_limit, max_bounding_box_limit, inputs)

        if write_to_db and isinstance(inputs[0], ShapeGenInputDto):
            self.packing_problem_db_service.write_shape_gen_model_inputs_to_table(batch_id, inputs)

        return inputs