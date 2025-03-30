import mydb
import sqlite3
from datetime import datetime


def insert_project(name, environment):
    conn = mydb.connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, environment, current_version_id) VALUES (?, ?, -1)", (name, environment))
    conn.commit()
    conn.close()


def get_projects():
    conn = mydb.connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return result


def get_project_by_name(project_name, project_env):
    conn = mydb.connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE name = ? and environment = ? limit 1",
                   (project_name, project_env))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return result


def update_project_current_version(id, current_version_id):
    conn = mydb.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE projects
        SET current_version_id = ?
        WHERE id = ?;
    ''', (current_version_id, id))
    conn.commit()
    conn.close()


def update_project_version_next(id, next_id):
    conn = mydb.connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE project_versions
        SET next_id = ?
        WHERE id = ?;
    ''', (next_id, id))
    conn.commit()
    conn.close()


def insert_project_version(project_id, version, url, last_id=None, next_id=None):
    conn = mydb.connect_db()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO project_versions (
            project_id, version, url,
            created_at, last_id, next_id
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (project_id, version, url, created_at, last_id, next_id))
    conn.commit()
    conn.close()

    return cursor.lastrowid


def update_project_version_next(id, next_id):
    conn = mydb.connect_db()
    cursor = conn.cursor()
    created_at = datetime.now().isoformat()
    cursor.execute('''
        UPDATE project_versions
        SET next_id = ?
        WHERE id = ?;
    ''', (next_id, id))
    conn.commit()
    conn.close()


def get_project_versioin(project_version_id):
    conn = mydb.connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_versions WHERE id = ? ",
                   (project_version_id,))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return result


def get_project_version_by_name(project_name, project_env):
    conn = mydb.connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project_versions WHERE project_id in (SELECT id FROM projects WHERE name = ? and environment = ?)",
                   (project_name, project_env))
    rows = cursor.fetchall()
    conn.close()

    result = [dict(row) for row in rows]
    return result
