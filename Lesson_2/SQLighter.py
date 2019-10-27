import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """Get all rows"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM music").fetchall()

    def select_single(self, rownum):
        """Get one row by rownum"""
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM music WHERE id = ?", (rownum,)
            ).fetchall()[0]

    def count_rows(self):
        """Count amount or rows"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM music").fetchall()
            return len(result)

    def close(self):
        """Close db connection"""
        self.connection.close()
