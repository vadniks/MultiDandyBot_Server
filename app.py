from flask import Flask, request as rq, jsonify, Response
import sync as sk

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Working</h1>'


@app.route('/new', methods=['POST'])
def newPlayer() -> Response:
    a = rq.json

    p = sk.registerNewPlayer(a['name'], a['script'])
    s: sk.Session = p.session

    return jsonify({'sid': s.sid, 'pid': p.id})


@app.route('/chk/<pid>', methods=['GET'])
def checkForPlayers(pid: int) -> Response:
    scripts = sk.getScripts(int(pid))
    return jsonify(scripts)


@app.route('/qt/<pid>', methods=['POST'])
def playerQuit(pid: int):
    return Response(status=200 if sk.removePlayer(int(pid)) else 404)


if __name__ == '__main__':
    app.run()
