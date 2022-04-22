from typing import List, Tuple

from flask import Flask, request as rq, jsonify, Response
import sync as sk

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Working</h1>'


@app.route('/new', methods=['POST'])
def newPlayer() -> Response:
    a = rq.json

    p = sk.Player(a['name'], a['script'], int(a['level']))
    sid, pid = sk.registerNewPlayer(p)

    return jsonify({'sid': sid, 'pid': pid})


@app.route('/chk/<pid>', methods=['GET'])
def checkForPlayers(pid: str) -> Response:
    players = sk.getPlayers(int(pid))
    return jsonify(players)


@app.route('/qt/<pid>', methods=['POST'])
def playerQuit(pid: str) -> Response:
    return Response(status=200 if sk.removePlayer(int(pid)) else 404)


@app.route('/trc/<sid>/<pid>', methods=['GET'])
def trace(sid: str, pid: str) -> Response:
    positions = sk.trace(int(sid), int(pid))
    return jsonify(positions) if positions is not None else Response(status=404)


@app.route('/upd/<pid>', methods=['POST'])
def updateLvl(pid: str) -> Response:
    a = rq.json
    sk.updatePlayer(int(pid), int(a['level']), int(a['x']), int(a['y']), int(a['gold']))
    return Response(status=200)


@app.route('', methods=['POST']) #        level goldAmount
def updateBoards(sid: str, gib: List[Tuple[int, int]]) -> Response: # gib goldInBoards
    pass #TODO

if __name__ == '__main__':
    app.run()
