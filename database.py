import sqlite3 as sq
import threading
from pathlib import Path
from typing import Callable, Any
from executor import TaskExecutor
from sync import Player
import atexit as ax
import sys
from threading import get_ident

_DIR_PATH = Path().resolve().absolute().__str__()
_DB_NAME = 'players' # and table name too
_DB_FILE = _DIR_PATH + _DB_NAME + '.db'
_DB_ID = 'id'
_DB_PLAYER = 'player'
_DB_SCORE = 'score'
_DB_SCRIPT = 'script'
_DB_DATE = 'date'

_executor: TaskExecutor
_connection: sq.Connection


def _wrapper(wrapped: Callable, doPost: Callable = None) -> Any:
    cursor = _connection.cursor()
    a = wrapped(cursor)
    _connection.commit()
    cursor.close()
    if doPost is not None: doPost(a)
    return a


# noinspection SqlNoDataSourceInspection
def _initializeTable(): _wrapper(lambda cursor:
    cursor.execute(f'''create table if not exists {_DB_NAME} (
        {_DB_ID} integer primary key, /*implicit autoincrement, pass null when inserting*/
        {_DB_PLAYER} text,
        {_DB_SCORE} integer,
        {_DB_SCRIPT} text,
        {_DB_DATE} integer
    )'''))


# noinspection SqlNoDataSourceInspection
def _insert(player: Player): _wrapper(lambda cursor:
    cursor.execute(f'''insert into {_DB_NAME} values (
        null,
        {player.name},
        {player.goldAmount},
        {player.script},
        {player.created}
    )'''))


# noinspection SqlNoDataSourceInspection
def _select() -> Any: return _wrapper(lambda cursor:
    cursor.execute(f'''select * from {_DB_NAME} order by {_DB_SCORE} desc'''))


def _init():
    global _connection, _executor

    sys.stderr.write('init ' + str(get_ident()) + '\n')

    def atExit():
        _connection.close()
        _executor.join()
    ax.register(lambda: _executor.doPost(False, lambda _: atExit(), None))  # TODO: make client's quit request sending in this way

    _connection = sq.connect(_DB_FILE)
    _initializeTable()


def _wrapper2(arg: Any | None, fun: Callable):
    sys.stderr.write('wrapper2 ' + str(get_ident()) + '\n')
    _id = _executor.doPost(True, lambda a: fun(a) if a is not None else fun(), arg)
    while (result := _executor.checkTask(_id)) is None: pass #sys.stderr.write(str(type(result)) + '\n')
    return result


def insert(player: Player): _wrapper2(player, _insert)


def select():
    sys.stderr.write('select ' + str(get_ident()) + '\n')
    return _wrapper2(None, _select)


sys.stderr.write('module ' + str(get_ident()) + '\n')
_executor = TaskExecutor()
_executor.daemon = True
_executor.start()
_executor.doPost(True, lambda _: _init(), None)
