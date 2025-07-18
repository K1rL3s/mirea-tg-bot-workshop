import sqlite3
from contextlib import closing
from dataclasses import dataclass


@dataclass
class User:
    id: str
    tg_id: int


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
                    id STRING PRIMARY KEY,
                    tg_id INTEGER NOT NULL
                )
            """)
            self.connection.commit()

    def save_user(self, id: str, tg_id: int) -> None:
        with closing(self.connection.cursor()) as cursor:
            if self.get_user_by_tg_id(tg_id) is None:
                cursor.execute("""
                    INSERT INTO users (id, tg_id)
                    VALUES (?, ?)
                """, (id, tg_id))
                self.connection.commit()

    def get_user_by_tg_id(self, tg_id: int) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            data = cursor.fetchone()
            return User(*data) if data else None

    def get_user_by_id(self, id: str) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
            data = cursor.fetchone()
            return User(*data) if data else None

    def get_all_users(self) -> list[User]:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()
            return [User(*row) for row in data]
