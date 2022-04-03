from flask import Flask, render_template, request
import io
import base64
from frontend.graph import make_graphic
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def get_stats():
    uploaded_files = request.files.getlist("file[]")

    im, num_replays = make_graphic(uploaded_files)

    if num_replays == 0:
        return render_template("index.html")

    data = io.BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("stats.html", img_data=encoded_img_data.decode('utf-8'), m=num_replays)


if __name__ == '__main__':
    app.run(debug=True)
