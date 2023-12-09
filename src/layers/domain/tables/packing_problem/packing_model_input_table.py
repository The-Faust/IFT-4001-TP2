from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy_utils import UUIDType

from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase


class PackingModelInputTable(PackingProblemBase().serve_base()):
    __tablename__ = 'packing_model_input'
    batch_id = Column(
        UUIDType(binary=False),
        ForeignKey('shape_gen_input.batch_id', ondelete='CASCADE'),
        primary_key=True
    )
    shape_gen_input_id = Column(
        UUIDType(binary=False),
        ForeignKey('shape_gen_input.input_id', ondelete='CASCADE'),
        primary_key=True
    )
    input_id = Column(UUIDType(binary=False), primary_key=True)
    inputs = Column(JSON)