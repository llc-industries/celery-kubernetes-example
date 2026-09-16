"""
SQLite database interface.
"""
import sqlite3
import time

import settings

sql_schema = """
create table if not exists tasks (
  id        text     primary key,
  created   real     not null
);
"""

def connect_db():
    return sqlite3.connect(settings.database_path)

def init():
    connection = connect_db()
    connection.executescript(sql_schema.strip())
    connection.commit()

def create_task(task_id):
    connection = connect_db()
    connection.execute("insert or replace into tasks (id, created) values (?, ?)", [str(task_id), time.time()])
    connection.commit()
    return task_id

def get_all():
    connection = connect_db()
    return (connection
            .execute("select id, created from tasks order by created asc")
            .fetchall())
