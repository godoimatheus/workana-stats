import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def album():
    imagens = os.listdir('static')
    return render_template('index.html', imagens=imagens)


if __name__ == '__main__':
    app.run(debug=True)
