import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    return flask.send_file('fig11.png')


if __name__ == '__main__':
    app.run(debug=True)

