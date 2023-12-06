from pathlib import Path
from typing import Union

from src.layers.domain import PackingModel


class PackingModelFactory:
    def make_packing_model(self, files: Union[str, Path] = None):
        shape_gen_model_attributes = dict()

        if files is not None:
            shape_gen_model_attributes['files'] = files

        return PackingModel(files)
