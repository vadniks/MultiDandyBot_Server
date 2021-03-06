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

from flask import Flask, request as rq, jsonify, Response
import sync as sk
import logging
import database as db

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARN)
app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>There are no easter eggs up here, go away.</h1>"


@app.route('/new', methods=['POST']) # TODO: define request methods in constants
def newPlayer() -> Response:
    a = rq.json

    p = sk.Player(a['name'], a['script'], int(a['level']))
    if sk.checkName(p.name) or db.checkName(p.name):
        return jsonify({'sid': sk.NUM_UNDEF})

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
    return Response(status=200) # TODO: define arguments names in constants


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
def getGoldAmount(sid: str, lvl: str) -> str | Response:
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


@app.route('/rd/<pid>', methods=['POST'])
def ready(pid: str) -> Response:
    sk.markReady(int(pid))
    return Response(status=200)


@app.route('/hpl/<pid>/<sid>', methods=['GET'])
def hasPlayerLeft(pid: str, sid: str) -> str:
    return str(sk.hasPlayerLeft(int(pid), int(sid)))


# TODO: to gracefully shutdown the server send a post request to the
# TODO: shutdown endpoint "curl -X POST http://127.0.0.1:5000/end"
# TODO: and then send the SIGTERM signal or Ctrl+C (SIGINT)
@app.route('/end', methods=['POST'])
def end() -> Response:
    db.end()
    return Response(status=200)


if __name__ == '__main__':
    app.run()
