from sqlalchemy import Column, ForeignKey, JSON, String, Date
from sqlalchemy_utils import UUIDType

from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase
from src.layers.domain.tables.packing_problem.shape_gen_model_input_table import ShapeGenModelInputTable


class PackingModelInputTable(PackingProblemBase().serve_base()):
    __tablename__ = 'packing_model_input'
    batch_name = Column(String, primary_key=True)
    batch_id = Column(
        UUIDType(binary=False),
        primary_key=True,
        unique=False
    )
    shape_gen_input_id = Column(
        UUIDType(binary=False),
        ForeignKey(ShapeGenModelInputTable.__table__.c.input_id, ondelete='CASCADE'),
        primary_key=True,
        unique=True
    )
    input_id = Column(UUIDType(binary=False), primary_key=True, unique=True)
    inputs = Column(JSON)
    generation_time = Column(Date)
