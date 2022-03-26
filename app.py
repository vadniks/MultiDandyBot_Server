from flask import Flask, request as rq, jsonify, Response

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Working</h1>'


@app.route('/new', methods=['POST'])
def newSession() -> Response:
    a = rq.json
    print(a['name'], a['script'])
    return jsonify({'sid': -1})


@app.route('/chk/<sid>', methods=['GET'])
def checkForPlayers(sid: int):
    return False


if __name__ == '__main__':
    app.run()
