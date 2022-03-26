from flask import Flask, request as rq, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Working</h1>'


@app.route('/new', methods=['POST'])
def newSession():
    a = rq.json
    print(a['name'], a['script'])
    return jsonify({'sid': -1})


if __name__ == '__main__':
    app.run()
