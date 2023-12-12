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
    
    
    usecase = SolvePackingUseCase()
    solution,data = usecase.execute('test_batch', (3, 3), (6, 6), 1, False)
    
    visualisateur = VisualisationService()
    visualisateur.set_shape_infos(data['rectSize'],data['rectOffset'],data['shape'],data['validShapes'],data['u'],data['l'])
    visualisateur.draw_all_shape()
    visualisateur.draw_solution(solution['x'],solution['kind'])
    plt.show()
    

if __name__ == "__main__":
    main()
