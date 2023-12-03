import logging

from src.layers.application.services.data_gen_service import DataGenService


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    # def test_datagen():
    #     data_gen_service = DataGenService()
    #     data_gen_service.generate(n_shapes=5, max_number_of_parts=3)

    # test_datagen()

    print('Hello World!')

if __name__ == "__main__":
    main()
