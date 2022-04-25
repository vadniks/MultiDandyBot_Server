import sqlite3 as sq
from pathlib import Path
from typing import Callable

from sync import Player
import atexit as ax

_DIR_PATH = Path().resolve().absolute().__str__()
_DB_NAME = 'players' # and table name too
_DB_FILE = _DIR_PATH + _DB_NAME + '.db'
_DB_ID = 'id'
_DB_PLAYER = 'player'
_DB_SCORE = 'score'
_DB_SCRIPT = 'script'
_DB_DATE = 'date'

_connection = sq.connect(_DB_FILE)
ax.register(lambda: _connection.close()) #TODO: make client's quit request sending in this way


def _wrapper(wrapped: Callable):
    cursor = _connection.cursor()
    wrapped(cursor)
    _connection.commit()
    cursor.close()


# noinspection SqlNoDataSourceInspection
def createTable(): _wrapper(lambda cursor:
    cursor.execute(f'''create table if not exists {_DB_NAME} (
        {_DB_ID} integer primary key, /*implicit autoincrement, pass null when inserting*/
        {_DB_PLAYER} text,
        {_DB_SCORE} integer,
        {_DB_SCRIPT} text,
        {_DB_DATE} integer
    )'''))


# noinspection SqlNoDataSourceInspection
def insert(player: Player): _wrapper(lambda cursor:
    cursor.execute(f'''insert into {_DB_NAME} values (
        null,
        {player.name},
        {player.goldAmount},
        {player.script},
        {player.created}
    )'''))
