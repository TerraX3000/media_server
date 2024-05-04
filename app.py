from flask import Flask, render_template, Response
import os

app = Flask(__name__)


@app.route("/")
@app.route("/<video_file>")
def index(video_file="video.mp4"):
    return render_template("video.html", video_file=video_file)


def generate_video(video_file):
    video_path = os.path.join("videos", video_file)
    with open(video_path, "rb") as video_file:
        while True:
            data = video_file.read(1024)
            if not data:
                break
            yield data


@app.route("/video")
@app.route("/video/<video_file>")
def video(video_file="video.mp4"):
    return Response(generate_video(video_file), mimetype="video/mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
