import logging
from typing import Type, Tuple

from sqlalchemy import MetaData, Engine, create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base


class PostgresBase:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_metadata_and_base(self, schema) -> Tuple[MetaData, Type[DeclarativeMeta]]:
        metadata = MetaData(schema)
        base = declarative_base(metadata=metadata)

        self.logger.debug(base)

        return metadata, base

    def get_engine(self, database: str) -> Engine:
        # TODO: Si temps mettre ces info dans un fichier de configuration
        user = 'postgres'
        password = 'postgres123'
        host = 'postgtres'
        port = 5432
        database = 'packing_problem'

        conn_str = f'postgresql://{user}:{password}@{host}:{port}/{database}'
        engine = create_engine(conn_str)

        return engine