import sqlite3
from contextlib import closing

type User = tuple[int, str | None, int | None]


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
                    name TEXT,
                    age INTEGER
                )
            """)
            self.connection.commit()

    def save_user(self, tg_id: int) -> None:
        with closing(self.connection.cursor()) as cursor:
            if self.get_user(tg_id) is None:
                cursor.execute("""
                    INSERT OR REPLACE INTO users (tg_id)
                    VALUES (?)
                """, (tg_id,))
                self.connection.commit()

    def get_user(self, tg_id: int) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            return cursor.fetchone()