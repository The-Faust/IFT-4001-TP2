import logging
from os import listdir
from pathlib import Path

from minizinc.driver import Driver

from src.layers.application.services.data_gen_service import DataGenService


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    # path_to_driver = Path('/minizinc', 'bin')
    # my_driver = Driver(path_to_driver)
    # my_driver.make_default()

    def test_datagen():
        data_gen_service = DataGenService()
        data_gen_service.generate()

    test_datagen()


if __name__ == "__main__":
    main()
