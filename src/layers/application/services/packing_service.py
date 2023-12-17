import logging
from datetime import timedelta

from minizinc import Solver, Instance

from src.layers.application.factories.packing_model_factory import PackingModelFactory
from src.layers.domain.inputs import PackingModelInput
from src.layers.domain.solutions import PackingModelSolution


class PackingService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.packing_model_factory: PackingModelFactory = PackingModelFactory()

    def solve(
            self,
            packing_model_inputs: PackingModelInput,
            solver: str = 'chuffed',
            timeout: int = 600,
    ) -> PackingModelSolution:
        solver = Solver.lookup(solver)
        model = self.packing_model_factory.make_packing_model()
        instance = Instance(solver, model)

        #  Il est mieux d'être clair lorsqu'on interagi avec minizinc sur quelle valeur est quoi
        instance['nObjects'] = packing_model_inputs.nObjects
        instance['nRectangles'] = packing_model_inputs.nRectangles
        instance['nShapes'] = packing_model_inputs.nShapes
        instance['rectSize'] = packing_model_inputs.rectSize
        instance['rectOffset'] = packing_model_inputs.rectOffset
        instance['shape'] = packing_model_inputs.shape
        instance['validShapes'] = packing_model_inputs.validShapes
        instance['l'] = packing_model_inputs.l
        instance['u'] = packing_model_inputs.u

        solution = instance.solve(timeout=timedelta(timeout), free_search=True)

        return PackingModelSolution(
            objective=solution['objective'],
            x=solution['x'],
            kind=solution['kind'],
            chosen_objects=solution['chosen_objects'],
            chosen_objects_count=solution['chosen_objects_count'],
            surface=solution['surface']
        )



