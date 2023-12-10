import logging
from typing import Type, Iterable
from uuid import uuid4

import sqlalchemy

from src.layers.application.factories.packing_problem_db_row_factory import PackingProblemDbRowFactory
from src.layers.domain.dtos import ShapeGenInputDto
from src.layers.domain.inputs import PackingModelInput
from src.layers.domain.tables.packing_problem.packing_model_input_table import PackingModelInputTable
from src.layers.domain.tables.packing_problem.packing_problem_base import PackingProblemBase
from src.layers.domain.tables.packing_problem.packing_project_engine import PackingProjectEngine
from src.layers.domain.tables.packing_problem.shape_gen_model_input_table import ShapeGenModelInputTable
from src.layers.infrastructure.postgres_repository import PostgresRepository


class PackingProblemDbService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = PackingProjectEngine().serve_engine()
        self.row_factory: PackingProblemDbRowFactory = PackingProblemDbRowFactory()
        self.postgres_repository: PostgresRepository = PostgresRepository(self.engine)

        self.create_schema_if_does_not_exists('inputs')
        self.create_table_if_does_not_exists(ShapeGenModelInputTable)
        self.create_table_if_does_not_exists(PackingModelInputTable)

    def get_batches_list(self):
        query = self.postgres_repository.session.query(ShapeGenModelInputTable.batch_id)

        return query.all()

    def write_packing_model_inputs_to_table(
        self,
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_id: uuid4,
        packing_model_inputs: Iterable[PackingModelInput],
        write_to_db: bool
    ) -> Iterable[PackingModelInputTable]:
        rows = self.row_factory \
            .make_packing_model_input_rows(batch_name, batch_id, shape_gen_input_id, packing_model_inputs)
        self.postgres_repository.add_rows(rows)

        if write_to_db:
            self.postgres_repository.commit()

        return rows

    def write_shape_gen_model_inputs_to_table(
        self,
        batch_name: str,
        batch_id: uuid4,
        shape_gen_input_dtos: Iterable[ShapeGenInputDto],
        write_to_db: bool
    ) -> Iterable[ShapeGenModelInputTable]:
        rows = self.row_factory.make_shape_gen_input_rows(batch_name, batch_id, shape_gen_input_dtos)
        self.logger.debug(rows)
        self.postgres_repository.add_rows(rows)

        if write_to_db:
            self.postgres_repository.commit()

        out_rows = self.postgres_repository.session \
            .query(ShapeGenModelInputTable) \
            .filter(ShapeGenModelInputTable.batch_id == batch_id) \
            .all()

        return [row.__dict__ for row in out_rows]

    def create_table_if_does_not_exists(self, table_object: Type[(PackingProblemBase().serve_base(),)]):
        table = table_object.__table__
        table_name = table.name

        with self.engine.connect() as conn:
            if not conn.dialect.has_table(conn, table_name):
                PackingProblemBase().serve_metadata().create_all(conn, tables=[table])
                conn.commit()

    def create_schema_if_does_not_exists(self, schema: str):
        with self.engine.connect() as conn:
            if not conn.dialect.has_schema(conn, schema):
                conn.execute(sqlalchemy.schema.CreateSchema(schema))
                conn.commit()
