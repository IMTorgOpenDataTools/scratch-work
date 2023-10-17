from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/static')
def serve_static(path):
    return send_from_directory('static', path)