from typing import Tuple

from src.layers.application.services.data_gen_service import DataGenService


class GenerateShapeGenInputUseCase:
    def __init__(self):
        self.data_gen_service: DataGenService = DataGenService()

    def execute(self, min_bounding_box_limit: Tuple[int, int], max_bounding_box_limit: Tuple[int, int]):
        self.data_gen_service.randomly_generate_shape_model_input(min_bounding_box_limit, max_bounding_box_limit)
