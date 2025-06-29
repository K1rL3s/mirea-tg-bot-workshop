import sqlite3
from contextlib import closing

type User = tuple[int, int, str, int]


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
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)
            self.connection.commit()

    def save_user(self, tg_id: int, name: str, age: int) -> int:
        with closing(self.connection.cursor()) as cursor:
            if self.get_user(tg_id) is None:
                cursor.execute("""
                    INSERT OR REPLACE INTO users (tg_id, name, age)
                    VALUES (?, ?, ?)
                    RETURNING id
                """, (tg_id, name, age))
                user_id = cursor.fetchone()
                self.connection.commit()
            return user_id

    def get_user_by_tg_id(self, tg_id: int) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            return cursor.fetchone()

    def get_user_by_id(self, id: int) -> User | None:
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
            return cursor.fetchone()

    def get_all_users(self) -> list[User]:
        with closing(self.connection.cursor()) as cursor:
            cursor = cursor.execute("SELECT * FROM users ORDER BY id")
            return cursor.fetchall()
