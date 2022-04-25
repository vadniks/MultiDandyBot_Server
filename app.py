from flask import Flask, request as rq, jsonify, Response
import sync as sk
import logging
import database as db

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARN)
app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>There's no easter eggs up here, go away.</h1>"


@app.route('/new', methods=['POST'])
def newPlayer() -> Response:
    a = rq.json

    p = sk.Player(a['name'], a['script'], int(a['level']))
    if sk.checkName(p.name):
        return jsonify({'sid': -1})

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


@app.route('/brd/<sid>/<lvl>', methods=['POST'])
def updateBoard(sid: str, lvl: str) -> Response:
    a = rq.json
    sk.updateBoard(int(sid), int(lvl), (int(a['pid']), int(a['gtf_x']), int(a['gtf_y'])))
    return Response(status=200)


@app.route('/trc_b/<sid>/<pid>/<lvl>', methods=['GET'])
def traceBoard(sid: str, pid: str, lvl: str) -> Response:
    takens = sk.traceBoard(int(sid), int(pid), int(lvl))
    return jsonify(takens) if takens is not None else Response(status=500)


@app.route('/gld/<sid>/<lvl>', methods=['GET'])
def getGoldAmount(sid: str, lvl: str) -> Response:
    a = sk.getGoldAmount(int(sid), int(lvl))
    return str(a) if a >= 0 else Response(status=500)


@app.route('/db', methods=['GET', 'POST'])
def dbOperations() -> Response:
    jsn = rq.json

    def onInsert():
        db.insert(sk.getPlayer(int(jsn['pid'])))
        return Response(status=200)

    return {
        'select': lambda: jsonify(db.select()),
        'insert': onInsert
    }[jsn['mode']]()


if __name__ == '__main__':
    app.run()
