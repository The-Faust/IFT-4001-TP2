import logging
from os import listdir
from pathlib import Path
from matplotlib import pyplot as plt

from minizinc.driver import Driver

from src.layers.application.usecases.solve_packing_usecase import SolvePackingUseCase
from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_service import PackingService
from src.layers.application.services.visualisation_service import VisualisationService

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    def test_generate_shape_gen_inputs_usecase():
        usecase = SolvePackingUseCase()
        usecase.execute('test_batch', (3, 3), (6, 6), 1, False)

        print('executed test_generate_shape_gen_inputs_usecase')

    test_generate_shape_gen_inputs_usecase()


if __name__ == "__main__":
    main()
