"""Entry point for the SGT Cart backend.

Dev server:        python run.py
Flask CLI / DB:    flask --app run db <command>

The server is started through Flask-SocketIO so WebSocket events work
alongside ordinary HTTP requests.
"""
from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(
        app, host="127.0.0.1", port=5000,
        debug=app.config["DEBUG"], allow_unsafe_werkzeug=True,
    )
