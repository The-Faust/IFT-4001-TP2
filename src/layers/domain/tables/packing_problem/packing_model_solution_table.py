from sqlalchemy import Column, JSON, Date, String
from sqlalchemy_utils import UUIDType

from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase


class PackingModelSolutionTable(PackingProblemBase().serve_base()):
    __tablename__ = 'packing_model_solution'
    batch_name = Column(String, primary_key=True)
    batch_id = Column(
        UUIDType(binary=False),
        primary_key=True
    )
    packing_model_input_id = Column(
        UUIDType(binary=False),
        primary_key=True
    )
    input_id = Column(UUIDType(UUIDType(binary=False)), primary_key=True)
    inputs = Column(JSON)
    generation_time = Column(Date)
