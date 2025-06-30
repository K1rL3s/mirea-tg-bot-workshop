import sqlite3
from contextlib import closing
from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    name: str
    age: int


class Database:
    def __init__(self, db_path: str) -> None:
        self.connection = sqlite3.connect(db_path)
        self._setup()

    def close(self) -> None:
        self.connection.close()

    def _setup(self) -> None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    tg_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)
            self.connection.commit()

    def save_user(self, tg_id: int, name: str, age: int) -> None:
        with closing(self.connection.cursor()) as cursor:
            if self.get_user(tg_id) is None:
                cursor.execute("""
                    INSERT OR REPLACE INTO users (tg_id, name, age)
                    VALUES (?, ?, ?)
                """, (tg_id, name, age))
                self.connection.commit()

    def get_user(self, tg_id: int) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            data = cursor.fetchone()
            return User(*data) if data else None
