from sqlalchemy import Column, JSON
from sqlalchemy_utils import UUIDType

from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase


class ShapeGenModelInputTable(PackingProblemBase().serve_base()):
    __tablename__ = 'shape_gen_model_input'
    batch_id = Column(UUIDType(binary=False), primary_key=True)
    input_id = Column(UUIDType(binary=False), primary_key=True)
    inputs = Column(JSON)
