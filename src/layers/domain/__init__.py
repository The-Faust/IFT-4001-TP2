from minizinc import Model
from pathlib import Path


class PackingModel(Model):
    def __init__(self, path_to_mzn: Path = Path('minizinc', 'model.mzn')):
        super().__init__([path_to_mzn])
