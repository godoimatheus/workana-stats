import flask
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("index.html")


@app.route('/1')
def fig1():
    return flask.send_file('fig1.png')


if __name__ == '__main__':
    app.run(debug=True)
