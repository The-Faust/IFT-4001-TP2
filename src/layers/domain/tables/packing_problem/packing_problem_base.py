from src.layers.domain.tables.postgres_base import PostgresBase


class PackingProblemBase:
    def __init__(self):
        postgres_base: PostgresBase = PostgresBase()

        self.metadata, self.base = postgres_base.get_metadata_and_base('inputs')

    def serve_metadata(self):
        return self.metadata

    def serve_base(self):
        return self.base