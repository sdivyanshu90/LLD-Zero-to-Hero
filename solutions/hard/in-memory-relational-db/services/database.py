from __future__ import annotations

import threading
from dataclasses import dataclass, field

from models.core import Row


@dataclass(slots=True)
class Table:
    rows: dict[str, Row] = field(default_factory=dict)
    _table_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def insert(self, row_id: str, values: dict[str, object]) -> None:
        with self._table_lock:
            if row_id in self.rows:
                raise ValueError(f"Row {row_id} already exists")
            self.rows[row_id] = Row(row_id=row_id, values=dict(values))

    def read(self, row_id: str) -> dict[str, object]:
        row = self._get_row(row_id)
        with row.lock:
            return dict(row.values)

    def update(self, row_id: str, values: dict[str, object]) -> None:
        row = self._get_row(row_id)
        with row.lock:
            row.values.update(values)

    def _get_row(self, row_id: str) -> Row:
        row = self.rows.get(row_id)
        if row is None:
            raise ValueError(f"Unknown row {row_id}")
        return row