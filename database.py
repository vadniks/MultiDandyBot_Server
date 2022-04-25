import sqlite3 as sq
import os.path as pt
from pathlib import Path
from sync import Player
import atexit as ax

_DIR_PATH = Path().resolve().absolute().__str__()
_DB_NAME = 'players'
_DB_FILE = _DIR_PATH + _DB_NAME + '.db'
_DB_ID = 'id'
_DB_PLAYER = 'player'
_DB_SCORE = 'score'
_DB_SCRIPT = 'script'

_connection = sq.connect(_DB_FILE)
ax.register(lambda: _connection.close()) #TODO: make client's quit request sending in this way


# noinspection SqlNoDataSourceInspection
def createTable():
    if pt.isfile(_DB_FILE): return

    cursor = _connection.cursor()
    cursor.execute(f'''create table {_DB_NAME} (
        {_DB_ID} integer primary key, /*implicit autoincrement, pass null when inserting*/
        {_DB_PLAYER} text,
        {_DB_SCORE} integer,
        {_DB_SCRIPT} text
    )''')
    _connection.commit()


def insert(player: Player):
    cursor = _connection.cursor()

