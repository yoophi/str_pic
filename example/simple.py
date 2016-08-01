from flask import Flask, render_template

from flask.ext.dummyimage import DummyImage

app = Flask(__name__)
dummyimage = DummyImage(app, url_prefix='/dm', endpoint='images', route='img')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
