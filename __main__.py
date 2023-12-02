import logging

from src.layers.application.services.data_gen_service import DataGenService


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    def test_datagen():
        data_gen_service = DataGenService()
        data_gen_service.generate()

    test_datagen()

    print('Hello World!')


if __name__ == "__main__":
    main()
