import flask
from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    return flask.send_file('fig1.png')


@app.route('/1')
def fig1():
    return flask.send_file('fig1.png')


if __name__ == '__main__':
    app.run(debug=True)
