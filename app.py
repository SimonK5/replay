from flask import Flask, request, send_from_directory
from stats.player_stats import get_stats
# from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend/build')


# cors = CORS()
# cors.init_app(app) a


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


# @app.route("/", methods=['POST'])
# def post_stats():
#     # uploaded_files = request.files.getlist("file[]")
#     #
#     # im, num_replays = make_graphic(uploaded_files)
#     #
#     # if num_replays == 0:
#     #     return render_template("index.html")
#     #
#     # data = io.BytesIO()
#     # im.save(data, "JPEG")
#     # encoded_img_data = base64.b64encode(data.getvalue())
#     #
#     # return render_template("stats.html", img_data=encoded_img_data.decode('utf-8'), m=num_replays)
#     # return get_stats(request.files.getlist("file[]"))
#     return get_stats(request.files.getlist("file[]"))


@app.route("/poststats", methods=["POST"], strict_slashes=False)
def post_stats():
    # print("test")
    data = request.get_json()
    # print("data:", data['replays'])
    # print("stats:", get_stats(data['replays']))
    return get_stats(data['replays'])


if __name__ == '__main__':
    app.run(debug=True)
