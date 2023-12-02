from pathlib import Path
from typing import Union

from src.layers.domain import ShapeGenModel


class ShapeGenModelFactory:
    def make_data_gen_model(self, files: Union[str, Path]):
        shape_gen_model_attributes = dict()

        if files is not None:
            shape_gen_model_attributes['files'] = files

        return ShapeGenModel(**shape_gen_model_attributes)
