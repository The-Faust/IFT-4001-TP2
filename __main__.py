import logging

from src.layers.application.usecases.solve_packing_usecase import SolvePackingUseCase
from src.layers.application.services.visualisation_service import VisualisationService
import time

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def main():
    logger.info('launching program')
    strdate = time.strftime("%Y-%m-%d_%H:%M:%S")
    batch_name = f"test_batch_{strdate}"

    logger.info('starting usecase execution')
    usecase = SolvePackingUseCase()
    data, solution = usecase.execute(
        batch_name=batch_name,
        min_bounding_box_limit=(4, 4),
        max_bounding_box_limit=(5, 5),
        n=1,
        write_to_db=False
    )

    logger.info('starting visualisation phase')
    visualisateur = VisualisationService()
    visualisateur.set_shape_infos(
        data[0]['inputs'].rectSize,
        data[0]['inputs'].rectOffset,
        data[0]['inputs'].shape,
        data[0]['inputs'].validShapes,
        data[0]['inputs'].u,
        data[0]['inputs'].l
    )
    visualisateur.draw_all_shape()
    visualisateur.draw_solution(solution[0]['inputs']['x'], solution[0]['inputs']['kind'])
    visualisateur.export(batch_name)

    logger.info('finished executing program')


if __name__ == "__main__":
    main()
