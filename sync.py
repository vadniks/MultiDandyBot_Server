from typing import List, Any
import time


class Player:
    id: int
    name: str
    script: str
    created: int
    session: Any # Session

    def __init__(S, _id: int, name: str, script: str, session: Any):
        S.id = _id
        S.name = name
        S.script = script
        S.session = session
        S.created = round(time.time() * 1000)


class Session:
    sid: int
    players: List[Player]
    created: int

    def __init__(S, sid: int):
        S.sid = sid
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
    a = Session(_sessionsAmount() + 1)
    _sessions.append(a)
    return a


def _getFreeSession() -> Session:
    global _sessions
    for i in sorted(_sessions, key=lambda j: j.created):
        if i.playersLen() <= MAX_PLAYERS_IN_SESSION:
            return i
    return _registerNewSession()


def _getSession(sid: int) -> Session:
    pass


def registerNewPlayer(name: str, script: str) -> Player:
    global _players
    s = _getFreeSession()

    p = Player(_playersAmount(), name, script, s)
    _players.append(p)

    return p


def getPlayer(pid: int) -> Player | None:
    global _players
    for i in _players:
        if i.id == pid:
            return i
    return None


def getScripts(pidToExclude: int) -> List[str]:
    global _players
    _list = []
    for i in _players:
        if i.id != pidToExclude:
            _list.append(i.script)
    return _list


def removePlayer(pid: int) -> bool:
    global _players
    for j, i in enumerate(_players):
        if i.id == pid:
            del _players[j]
            return True
    return False
