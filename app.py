from flask import Flask, request, send_from_directory
from stats.player_stats import get_stats
# from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend/build')


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/poststats", methods=["POST"], strict_slashes=False)
def post_stats():
    data = request.get_json()
    return get_stats(data['replays'])


if __name__ == '__main__':
    app.run(debug=True)
