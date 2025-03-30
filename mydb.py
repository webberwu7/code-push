import sqlite3
from datetime import datetime


def connect_db():
    return sqlite3.connect("mydb.db")


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            environment TEXT,
            current_version_id INTEGER,
            UNIQUE(name, environment)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            url TEXT,
            created_at TEXT NOT NULL,
            last_id INTEGER,
            next_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    ''')

    conn.commit()
    conn.close()


def init():
    create_tables()
