import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

class TaskRepository:
    def __init__(self, database='tarefas.db'):
        self.database = str(database)
        self.initialize()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def initialize(self):
        with self.connect() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL CHECK(length(trim(titulo)) BETWEEN 1 AND 100),
                descricao TEXT NOT NULL DEFAULT '',
                concluida INTEGER NOT NULL DEFAULT 0 CHECK(concluida IN (0,1)),
                criada_em TEXT NOT NULL)""")

    def list_all(self):
        with self.connect() as con:
            return [dict(r) for r in con.execute('SELECT * FROM tarefas ORDER BY concluida, id DESC')]

    def get(self, task_id):
        with self.connect() as con:
            row = con.execute('SELECT * FROM tarefas WHERE id=?', (task_id,)).fetchone()
            return dict(row) if row else None

    def add(self, title, description=''):
        title = title.strip()
        description = description.strip()
        if not 1 <= len(title) <= 100: raise ValueError('Título deve ter entre 1 e 100 caracteres.')
        if len(description) > 500: raise ValueError('Descrição deve ter até 500 caracteres.')
        with self.connect() as con:
            cursor = con.execute('INSERT INTO tarefas(titulo, descricao, criada_em) VALUES (?,?,?)',
                                 (title, description, datetime.now(timezone.utc).isoformat()))
            return cursor.lastrowid

    def update(self, task_id, title, description='', completed=False):
        title=title.strip();description=description.strip()
        if not 1 <= len(title) <= 100: raise ValueError('Título deve ter entre 1 e 100 caracteres.')
        if len(description) > 500: raise ValueError('Descrição deve ter até 500 caracteres.')
        with self.connect() as con:
            cursor=con.execute('UPDATE tarefas SET titulo=?,descricao=?,concluida=? WHERE id=?',
                               (title,description,int(bool(completed)),task_id))
            return cursor.rowcount > 0

    def delete(self, task_id):
        with self.connect() as con:
            return con.execute('DELETE FROM tarefas WHERE id=?',(task_id,)).rowcount > 0
