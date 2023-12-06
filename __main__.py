import logging
from os import listdir
from pathlib import Path

from minizinc.driver import Driver

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_service import PackingService


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
    print(data);
    def packing(_data):
        packing_service = PackingService()
        return packing_service.solve(_data)

    print(packing(data))

if __name__ == "__main__":
    main()
