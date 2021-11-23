import sqlite3


class DB:

    def __init__(self):
        self.conn = sqlite3.connect('66daysofdata.db')
        self.__init_tables()

    def __init_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS "acknowledgments" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "from_user_id"	INTEGER NOT NULL,
                    "to_user_id"	INTEGER NOT NULL,
                    "timestamp"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY("id" AUTOINCREMENT));''')

    def list_acknowledgments(self):
        return self.conn.execute(
            'SELECT to_user_id, COUNT(*) AS count FROM acknowledgments GROUP BY to_user_id ORDER BY count DESC LIMIT 10').fetchall()

    def add_acknowledgment(self, from_user_id: int, to_user_id: int):
        self.conn.execute('INSERT INTO acknowledgments (from_user_id, to_user_id) VALUES (?, ?)',
                          (from_user_id, to_user_id))
        self.conn.commit()

    def get_last_user_acknowledgment(self, from_user_id: int, to_user_id: int):
        last = self.conn.execute(
            'SELECT timestamp FROM acknowledgments WHERE from_user_id = ? AND to_user_id = ? ORDER BY id DESC LIMIT 1',
            (from_user_id, to_user_id)).fetchone()
        return last[0] if last is not None else None

    def delete_single_user_acknowledgment(self, to_user_id: int):
        self.conn.execute('DELETE FROM acknowledgments WHERE to_user_id = ? ORDER BY id DESC LIMIT 1', (to_user_id,))
