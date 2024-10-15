from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets

class IRWebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secrets.token_hex(16)
        self.socketio = SocketIO(self.app, async_mode='threading')  
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('overlay.html')

    def run(self, host="127.0.0.1", port=8085, debug=True):
        self.socketio.run(self.app, host=host, port=port, debug=debug)
