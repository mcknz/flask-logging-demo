"""logging demo app"""
from logging import config as logging_config

from flask import Flask, Response, render_template

from config import settings
from utils.timer import Timer

logging_config.dictConfig(settings.LOG_CONFIG)
timer = Timer()

APP = Flask(__name__, static_folder="app/static/", template_folder="app/static/")
@APP.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")

@APP.route("/timer_stream", methods=["GET"])
def timer_stream():
    """returns timer info to web page"""
    return Response(timer.get_time(), mimetype="text/plain", content_type="text/event-stream")

if __name__ == "__main__":
    APP.run(debug=True, host="0.0.0.0", port=1111, threaded=True)
