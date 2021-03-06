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

from typing import List, Any, Tuple
import time
from data import *

NUM_UNDEF = -1
THRESHOLD = 0.1 # seconds


# TODO: add time period between start and finish of the player's game
# TODO: from dataclasses import dataclass \n @dataclass
class Player:
    id: int
    name: str
    script: str
    created: int
    session: Any # Session
    level: int
    coords: Tuple[int, int] # x y
    goldAmount: int #TODO: rename to score
    isReady: bool

    def __init__(S,
        name: str,
        script: str,
        level: int
    ):
        S.id = NUM_UNDEF
        S.name = name
        S.script = script
        S.session = None
        S.created = round(time.time() * 1000)
        S.level = level
        S.goldAmount = 0
        S.isReady = False


class Board:
    id: int
    session: Any # Session
    level: int          #  pid   x    y
    goldTakens: List[Tuple[int, int, int]]
    created: int

    def __init__(S, _id: int, session: Any, level: int):
        S.id = _id
        S.session = session
        S.level = level
        S.goldTakens = []
        S.created = round(time.time() * 1000)


class Session:
    id: int
    players: List[Player]
    created: int
    boards: List[Board]

    def __init__(S, sid: int):
        S.id = sid
        S.created = round(time.time() * 1000)
        S.players = []
        S.boards = [Board(sid, S, i) for i in range(LEVELS_AMOUNT)]

    def playersLen(S) -> int: return len(S.players)


MAX_PLAYERS_IN_SESSION = 5
_sessions: List[Session] = []
_players: List[Player] = []


def _sessionsAmount() -> int:
    global _sessions
    return len(_sessions)


def _playersAmount() -> int:
    global _players
    return len(_players)


def _registerNewSession() -> Session:
    global _sessions
    a = Session(_sessionsAmount())
    _sessions.append(a)
    return a


# TODO: give new player new session if he connects after players
# TODO: in the last free session began their game
def _getFreeSession() -> Session:
    global _sessions
    for i in sorted(_sessions, key=lambda j: j.created):
        if i.playersLen() <= MAX_PLAYERS_IN_SESSION:
            return i
    return _registerNewSession()


#                                         sid  pid
def registerNewPlayer(p: Player) -> Tuple[int, int]:
    global _players
    s = _getFreeSession()

    p.id = _playersAmount()
    p.session = s

    lvl = LEVELS[p.level]
    p.coords = (lvl[XX], lvl[YY])

    _players.append(p)
    s.players.append(p)

    return s.id, p.id


def getPlayer(pid: int) -> Player | None:
    global _players
    for i in _players:
        if i.id == pid:
            return i
    return None


def getPlayers(pidToExclude: int) -> List[Tuple[int, str, bool]]:
    global _players
    _list = []
    for i in _players:
        if i.id != pidToExclude:
            _list.append((i.id, i.name, i.isReady))
    return _list


def delSessionIfNeeded(sid: int) -> bool:
    global _sessions
    for j, i in enumerate(_sessions):
        if i.id == sid and len(i.players) == 0:
            _sessions.pop(j)
            return True
    return False


def removePlayer(pid: int) -> bool:
    global _players
    for j, i in enumerate(_players):
        if i.id == pid:
            playersInSession = i.session.players
            for l, k in enumerate(playersInSession):
                if k.id == pid:
                    playersInSession.pop(l)

            _players.pop(j)
            delSessionIfNeeded(i.session.id)
            return True
    return False


def _getSession(sid: int) -> Session | None:
    for i in _sessions:
        if i.id == sid:
            return i
    return None


#                                           id   name lvl   x    y   gold
def trace(sid: int, pid: int) -> List[Tuple[int, str, int, int, int, int]] | None:
    global _players, _sessions

    session = _getSession(sid)
    if session is None: return None

    _list = []
    for i in session.players:
        if i.id != pid:
            _list.append((i.id, i.name, i.level, i.coords[0], i.coords[1], i.goldAmount))

    return _list


def updatePlayer(pid: int, level: int, x: int, y: int, gold: int):
    p = getPlayer(pid)
    assert p is not None
    p.level = level
    p.coords = (x, y)
    p.goldAmount = gold


#                                                          pid   x    y
def updateBoard(sid: int, level: int, goldTakenFrom: Tuple[int, int, int]):
    s = _getSession(sid)
    assert s is not None
    bs = s.boards
    bs[level].goldTakens.append(goldTakenFrom)


#                                                            pid   x    y
def traceBoard(sid: int, pid: int, level: int) -> List[Tuple[int, int, int]]:
    s = _getSession(sid)
    assert s is not None
    _list = []
    for i in s.boards[level].goldTakens:
        if i[0] != pid:
            _list.append(i)
    return _list


def getGoldAmount(sid: int, level: int) -> int:
    return LEVELS[level][GG] - len(_getSession(sid).boards[level].goldTakens)


def checkName(name: str) -> bool:
    for i in _players:
        if i.name == name:
            return True
    return False


def markReady(pid: int):
    for i in _players:
        if i.id == pid:
            i.isReady = True
            return
    raise Exception()


def hasPlayerLeft(pid: int, sid: int) -> bool:
    session = _getSession(sid)
    for i in session.players:
        if i.id == pid:
            return False
    return True
