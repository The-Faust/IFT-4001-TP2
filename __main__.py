import logging

from src.layers.application.usecases.generate_shape_gen_inputs_usecase import SolvePackingUseCase

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():
    def test_generate_shape_gen_inputs_usecase():
        usecase = SolvePackingUseCase()
        usecase.execute('test_batch', (2, 2), (10, 10), 10, False)

        print('executed test_generate_shape_gen_inputs_usecase')

    test_generate_shape_gen_inputs_usecase()


if __name__ == "__main__":
    main()
