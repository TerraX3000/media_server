from flask import Flask, render_template, Response
import os
import yaml
import json
from typing import Dict, List, Union

app = Flask(__name__)


def read_yaml(file_path) -> Union[Dict, List]:
    """Read the specified file and return as a dictionary or list."""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


@app.route("/media.json")
def media():
    file = "media_content.yaml"
    media_list = read_yaml(file)
    return json.dumps(media_list)


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
