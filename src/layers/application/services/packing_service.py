import logging
from datetime import timedelta
from pathlib import Path
from typing import Union

from minizinc import Solver, Instance, Model


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
        model = self.packing_model_factory.make_packing_model()
        instance = Instance(solver, model)
        #
        for key in data.keys():
            instance[key] = data[key]

        solution = instance.solve(timeout=timedelta(timeout), free_search=True)

        return solution



