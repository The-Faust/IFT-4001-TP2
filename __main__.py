import logging

from src.layers.application.services.data_gen_service import DataGenService
from src.layers.application.services.packing_service import PackingService


logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def main():

    def datagen():
        data_gen_service = DataGenService()
        return data_gen_service.generate_packing_model_inputs()

    data = datagen()
    print(data);
    def packing(_data):
        packing_service = PackingService()
        return packing_service.solve(_data)

    print(packing(data))

if __name__ == "__main__":
    main()
