import logging

from src.layers.domain.tables.postgres_base import PostgresBase


class PackingProjectEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        base: PostgresBase = PostgresBase()

        self.engine = base.get_engine()

    def serve_engine(self):
        return self.engine