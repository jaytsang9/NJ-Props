import os, requests
from flask import Flask, render_template, url_for, jsonify, request
app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['TRACK_MODIFICATIONS'] = False

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)