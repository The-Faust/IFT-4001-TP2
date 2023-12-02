from pathlib import Path
from typing import Union

from src.layers.domain import PackingModel


class PackingModelFactory:
    def make_packing_model(self, files: Union[str, Path] = None):
        return PackingModel(files)
