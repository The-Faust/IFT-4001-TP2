import logging
from os import listdir
from pathlib import Path

from minizinc.driver import Driver

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_service import PackingService
from src.layers.application.services.visualisation_service import VisualisationService

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    # path_to_driver = Path('/minizinc', 'bin')
    # my_driver = Driver(path_to_driver)
    # my_driver.make_default()

    def datagen():
        data_gen_service = DataGenService()
        return data_gen_service.generate()

    data = datagen()
    visualisateur = VisualisationService()
    visualisateur.set_shape_infos(data['rectSize'],data['rectOffset'],data['shape'],data['validShapes'])
    visualisateur.draw_all_shape()
    print(data)
    def packing(_data):
        packing_service = PackingService()
        return packing_service.solve(_data)

    solution = packing(data)
    print(solution)
    
    
    

if __name__ == "__main__":
    main()
