from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with open('cfg.json') as json_file:
        JSON = json.load(json_file)
        _host, _port = JSON["host"], JSON["port"]
    app.run(host=_host, port=_port)
