import logging
from os import listdir
from pathlib import Path

from minizinc.driver import Driver

from src.layers.application.usecases.solve_packing_usecase import SolvePackingUseCase
from src.layers.application.services.visualisation_service import VisualisationService
import time

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    strdate = time.strftime("%Y-%m-%d_%H:%M:%S")
    batch_name = f"test_batch_{strdate}"
    usecase = SolvePackingUseCase()
    data,solution = usecase.execute(batch_name, (3, 3), (6, 6), 1, False)
    
    visualisateur = VisualisationService()
    visualisateur.set_shape_infos(data[0]['inputs'].rectSize,
                                  data[0]['inputs'].rectOffset,
                                  data[0]['inputs'].shape,
                                  data[0]['inputs'].validShapes,
                                  data[0]['inputs'].u,
                                  data[0]['inputs'].l
                                  )
    visualisateur.draw_all_shape()
    visualisateur.draw_solution(solution[0]['inputs']['x'],solution[0]['inputs']['kind'])
    visualisateur.export(batch_name)

if __name__ == "__main__":
    main()
