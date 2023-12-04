import logging
from datetime import timedelta
from pathlib import Path
from typing import Tuple, Union, List

from minizinc import Solver, Instance, Model
from numpy.random import randint

from src.layers.application.factories.packing_model_factory import PackingModelFactory

class PackingService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.packing_model_factory: PackingModelFactory = PackingModelFactory()

    def solve(
            self,
            data : dict,
            solver: str = 'chuffed',
            timeout: int = 600,
            files: Union[str, Path] = None
    )-> any:
        solver = Solver.lookup(solver)
        #model = self.packing_model_factory.make_packing_model(files)
        model = Model("minizinc/packing/model.mzn")
        instance = Instance(solver, model)
        #
        for key in data.keys():
            instance[key] = data[key]
        # rectSize: List[List[int, int]] = [[1, 1], [1, 1]]

        # instance["nObjects"] = 1
        # instance["nRectangles"] = 1
        # instance["nShapes"] = 1
        # instance["rectSize"] = [[1,1]]#data["rectSize"]
        # instance["rectOffset"] = [[1,1]]#data["rectOffset"]
        # instance["shape"] = data["shape"]
        # instance["validShapes"] = data["validShapes"]
        # instance["l"] = [0,0]
        # instance["u"] = [10,10]


        solution = instance.solve(timeout=timedelta(timeout), free_search=True)
        print(solution)

        return solution



