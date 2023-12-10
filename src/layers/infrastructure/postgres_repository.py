from typing import Iterable, Dict, Tuple

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


class PostgresRepository:
    def __init__(self, engine: Engine):
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()

    def add_rows(self, rows: Iterable[Dict[str, any]]):
        if not isinstance(rows, Tuple):
            rows = tuple(rows)

        self.session.add_all(rows)

    def add_row(self, row: Dict[str, any]):
        self.session.add(row)

    def commit(self):
        self.session.commit()
