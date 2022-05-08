"""
MIT License

Copyright (c) 2022 Vad Nik (https://github.com/vadniks)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sqlite3 as sq
from pathlib import Path
from sqlite3 import Row
from time import sleep
from typing import Callable, Any, List
from executor import TaskExecutor
from sync import Player, THRESHOLD

_DIR_PATH = Path().resolve().absolute().__str__()
_DB_NAME = 'players' # and table name too
_DB_FILE = _DIR_PATH + '/' + _DB_NAME + '.db'
_DB_ID = 'id'
_DB_PLAYER = 'player'
_DB_SCORE = 'score'
_DB_SCRIPT = 'script'
_DB_DATE = 'date'

_executor: TaskExecutor
_connection: sq.Connection
_canWait = True


def _wrapper(wrapped: Callable) -> Any:
    cursor = _connection.cursor()
    a = wrapped(cursor)
    _connection.commit()
    cursor.close()
    return a


def _initializeTable(): _wrapper(lambda cursor:
    cursor.execute(f'''create table if not exists {_DB_NAME} (
        {_DB_ID} integer primary key, /*implicit autoincrement, pass null when inserting*/
        {_DB_PLAYER} text,
        {_DB_SCORE} integer,
        {_DB_SCRIPT} text,
        {_DB_DATE} integer
    )'''))


def _insert(player: Player): _wrapper(lambda cursor:
    cursor.execute(f'''insert into {_DB_NAME} (
        {_DB_PLAYER},
        {_DB_SCORE},
        {_DB_SCRIPT},
        {_DB_DATE}
    ) values (?, ?, ?, ?)''', (
        player.name,
        player.goldAmount,
        player.script,
        player.created)))


def _select() -> List[Row]: return _wrapper(lambda cursor:
    cursor.execute(f'''select 
        {_DB_PLAYER}, 
        {_DB_SCORE}
    from {_DB_NAME} order by {_DB_SCORE} desc''').fetchall())


def _checkName(name: str) -> Row: return _wrapper(lambda cursor:
    cursor.execute(f'select {_DB_ID} from {_DB_NAME} where {_DB_PLAYER} = ? limit 1',
        (name,)).fetchone())


def _init():
    global _connection
    _connection = sq.connect(_DB_FILE)
    _initializeTable()


def _wrapper2(arg: Any | None, fun: Callable) -> Any:
    global _canWait
    _id = _executor.doPost(True, lambda a: fun(a) if a is not None else fun(), arg)
    while (result := _executor.checkTask(_id)) is None and _canWait: sleep(THRESHOLD)
    return result


def insert(player: Player):
    global _executor
    _executor.doPost(False, _insert, player)


def select() -> List[Row]: return _wrapper2(None, _select)


def checkName(name: str) -> bool: return _wrapper2(name,
    lambda _name: _checkName(_name) is not None)


def end():
    global _executor

    def a(_):
        global _connection, _executor, _canWait
        _connection.close()
        _executor.end()
        _canWait = False
        exit(0)
    _executor.doPost(False, a, None)


_executor = TaskExecutor()
_executor.start()
_executor.doPost(False, lambda _: _init(), None)
