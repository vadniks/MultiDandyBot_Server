from typing import List, Any, Tuple
import time
from data import *

NUM_UNDEF = -1


class Player:
    id: int
    name: str
    script: str
    created: int
    session: Any # Session
    level: int
    coords: Tuple[int, int] # x y
    goldAmount: int

    def __init__(
        S,
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


class Session:
    id: int
    players: List[Player]
    created: int

    def __init__(S, sid: int):
        S.id = sid
        S.created = round(time.time() * 1000)
        S.players = []

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


def getPlayers(pidToExclude: int) -> List[Tuple[int, str]]:
    global _players
    _list = []
    for i in _players:
        if i.id != pidToExclude:
            _list.append((i.id, i.name))
    return _list


def removePlayer(pid: int) -> bool:
    global _players
    for j, i in enumerate(_players):
        if i.id == pid:
            del _players[j]
            return True
    return False


#                                           id   lvl   x    y   gold
def trace(sid: int, pid: int) -> List[Tuple[int, int, int, int, int]] | None:
    global _players, _sessions

    session = None
    for i in _sessions:
        if i.id == sid:
            session = i
    if session is None: return None

    _list = []
    for i in session.players:
        if i.id != pid:
            _list.append((i.id, i.level, i.coords[0], i.coords[1], i.goldAmount))

    return _list


def updatePlayer(pid: int, level: int, x: int, y: int, gold: int):
    p = getPlayer(pid)
    p.level = level
    p.coords = (x, y)
    p.goldAmount = gold
