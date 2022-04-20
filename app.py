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

    print(type(s))

    return jsonify({'sid': s.sid, 'pid': p.id})


@app.route('/chk/<pid>', methods=['GET'])
def checkForPlayers(pid: int) -> Response:
    scripts = sk.getScripts(pid)
    return jsonify(scripts)


if __name__ == '__main__':
    app.run()
