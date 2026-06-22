#based on https://flask.palletsprojects.com/en/stable/patterns/sqlite3/

import sqlite3
from flask import g

DATABASE = 'db/database.db'


def get_db():
    """
    Get the database (Connect to it)
    """

    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def disconnect_db():
    """
    Close the connection with the database
    """

    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """
    Execute a SQL query against the database.

    Example:
        >>> query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
    """

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv