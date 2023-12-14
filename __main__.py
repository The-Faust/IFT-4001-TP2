import logging
from os import listdir
from pathlib import Path
from matplotlib import pyplot as plt

from minizinc.driver import Driver

from src.layers.application.usecases.solve_packing_usecase import SolvePackingUseCase
from src.layers.application.services.visualisation_service import VisualisationService

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    
    
    usecase = SolvePackingUseCase()
    data,solution = usecase.execute('test_batch', (3, 3), (6, 6), 1, False)
    
    visualisateur = VisualisationService()
    visualisateur.set_shape_infos(data[0]['inputs'].rectSize,
                                  data[0]['inputs'].rectOffset,
                                  data[0]['inputs'].shape,
                                  data[0]['inputs'].validShapes,
                                  data[0]['inputs'].u,
                                  data[0]['inputs'].l
                                  )
    visualisateur.draw_all_shape()
    visualisateur.draw_solution(solution[0]['x'],solution[0]['kind'])
    plt.show()
    print("fin")
    
    with open(Path('visualisation_files', 'test.txt'), 'wt') as f:
        f.write('test 1 2')

if __name__ == "__main__":
    main()
