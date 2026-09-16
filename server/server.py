from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', JSON=JSON_FROM_BACKEND)


if __name__ == '__main__':

    JSON_FROM_BACKEND = [
        {
            "id": 1,
            "first_name": "Алексей",
            "last_name": "Понарин",
        },
        {
            "id": 2,
            "first_name": "Андрей",
            "last_name": "Руднев",
        },
        {
            "id": 3,
            "first_name": "Егор",
            "last_name": "Чагаев",
        },
        {
            "id": 4,
            "first_name": "Ярослав",
            "last_name": "Бессемянников",
        }
    ]

    with open('cfg.json') as json_file:
        JSON = json.load(json_file)
        _host, _port = JSON["host"], JSON["port"]
    app.run(host=_host, port=_port)
