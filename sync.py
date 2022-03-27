from typing import List


class Player:
    id: int
    name: str
    script: str

    def __init__(S, _id: int, name: str, script: str):
        S.id = _id
        S.name = name
        S.script = script


class Session:
    sid: int
    players: List[Player]

    def __init__(S, sid: int):
        S.sid = sid


_sessions: List[Session]


def _sessionsAmount() -> int:
    return _sessions.__len__()


def registerNewSession() -> Session:
    a = Session(_sessionsAmount() + 1)
    _sessions.append(a)
    return a


def _getFreeSession() -> Session:
    pass


def _getSession(sid: int) -> Session:
    pass


def waitForGameStart(sid: int) -> bool:
    pass


def registerNewPlayer(name: str, script: str) -> bool:
    s = _getFreeSession()
    if s is None:
        return False
