from minizinc import Model
from pathlib import Path


class PackingModel(Model):
    def __init__(self, files: Path = Path('minizinc', 'packing', 'model.mzn')):
        super().__init__(files)


class ShapeGenModel(Model):
    def __init__(self, files: Path = Path('minizinc', 'data_gen', 'shapeGen.mzn')):
        super().__init__(files)
