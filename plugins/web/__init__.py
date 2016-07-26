from threading import Thread
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_socketio import SocketIO, send, emit

from pokemongo_bot import logger, event_manager
from pokemongo_bot.event_manager import manager

def run_flask():
    app = Flask(__name__, static_url_path='')
    app.use_reloader = False
    app.config["SECRET_KEY"] = "OpenPoGoBot"
    socketio = SocketIO(app)

    logging_buffer = []

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.route("/js/<path:path>")
    def send_javascript():
        return send_from_directory("js", path)

    @app.route("/css/<path:path>")
    def send_stylesheet():
        return send_from_directory("css", path)

    @app.route("/images/<path:path>")
    def send_images():
        return send_from_directory("images", path)

    @app.route("/data/<path:path>")
    def send_data():
        return send_from_directory("data", path)

    @manager.on("logging_output")
    def logging_event(event_name, output, color):
        line = {"output": output, "color": color}
        logging_buffer.append(line)
        socketio.emit("logging", line, namespace="/event")

    @socketio.on("connect", namespace="/event")
    def connect():
        socketio.emit("logging", logging_buffer, namespace="/event")
        logger.log("Client connected", "yellow")

    @socketio.on("disconnect", namespace="/event")
    def disconnect():
        logger.log("Client disconnected", "yellow")

    socketio.run(app, host="0.0.0.0", port=8000)
t = Thread(target=run_flask)
t.daemon = True
t.start()
