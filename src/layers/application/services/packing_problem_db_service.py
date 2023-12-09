from typing import Type, Iterable
from uuid import uuid4

from src.layers.application.factories.packing_problem_db_row_factory import PackingProblemDbRowFactory
from src.layers.domain.dtos import ShapeGenInputDto
from src.layers.domain.inputs import PackingModelInput
from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase
from src.layers.domain.tables.packing_problem.packing_project_engine import PackingProjectEngine
from src.layers.domain.tables.packing_problem.shape_gen_model_input_table import ShapeGenModelInputTable
from src.layers.infrastructure.postgres_repository import PostgresRepository


class PackingProblemDbService:
    def __init__(self):
        self.engine = PackingProjectEngine().serve_engine()
        self.row_factory: PackingProblemDbRowFactory = PackingProblemDbRowFactory()
        self.postgres_repository: PostgresRepository = PostgresRepository(self.engine)

    def get_batches_list(self):
        query = self.postgres_repository.session.query(ShapeGenModelInputTable.batch_id)

        return query.all()

    def write_packing_model_inputs_to_table(
        self,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_inputs: Iterable[PackingModelInput]
    ):
        rows = self.row_factory \
            .make_packing_model_input_rows(batch_id, shape_gen_input_id, packing_model_inputs)
        self.postgres_repository.add_rows(rows)

    def write_shape_gen_model_inputs_to_table(
        self,
        batch_id: uuid4,
        shape_gen_input_dtos: Iterable[ShapeGenInputDto]
    ):
        rows = self.row_factory.make_shape_gen_input_rows(batch_id, shape_gen_input_dtos)
        self.postgres_repository.add_rows(rows)

    def create_table_if_does_not_exists(self, table_object: Type[(PackingProblemBase().serve_base(),)]):
        table_name = table_object.name

        if not self.engine.dialect.has_table(self.engine, table_name):
            PackingProblemBase().serve_metadata().create_all(self.engine, tables=[table_object])
