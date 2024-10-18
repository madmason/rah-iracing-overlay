from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets
import os
import sys

class IRWebApp:
    def __init__(self):
        """
        Initialize the Flask web application with a secret key and set up SocketIO with threading mode.
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secrets.token_hex(16)
        self.socketio = SocketIO(self.app, async_mode='threading')  
        self._setup_routes()

    def _setup_routes(self):
        """
        Define the routes for the web application.
        """
        @self.app.route('/input-telemetry')
        def index():
            return render_template('overlay.html')

    def run(self, host="127.0.0.1", port=8085, debug=True, use_reloader=False):
        """
        Run the Flask web application with the provided host, port, debug, and use_reloader settings.
        """
        self.socketio.run(self.app, host=host, port=port, debug=debug, use_reloader=use_reloader)

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, whether running from source or as a PyInstaller bundle. """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)