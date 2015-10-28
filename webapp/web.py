from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "success"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
