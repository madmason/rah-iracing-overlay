from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets

class IRWebApp:
    """
    A class that manages a Flask web application with SocketIO integration for real-time
    telemetry communication. The web application serves a telemetry interface and
    handles SocketIO connections.

    Attributes:
        app (Flask): The Flask web application instance.
        socketio (SocketIO): The SocketIO instance to handle real-time communication.
    """

    def __init__(self):
        """
        Initializes the IRWebApp class by setting up the Flask application and SocketIO.
        A secret key is generated for session management, and the route setup is called
        to define the web application routes.
        """
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a secure secret key
        self.socketio = SocketIO(self.app, async_mode='threading')  # Set up SocketIO with threading async mode
        self._setup_routes()  # Define the application routes

    def _setup_routes(self):
        """
        Defines the routes for the Flask web application. Currently, there is only one route
        that serves the telemetry overlay HTML page.

        Routes:
            /input-telemetry: Serves the telemetry overlay page.
        """
        @self.app.route('/input-telemetry')
        def index():
            """
            Route that renders the telemetry overlay HTML page.

            Returns:
                str: The HTML content of the overlay.html template.
            """
            return render_template('overlay.html')

    def run(self, host="127.0.0.1", port=8085, debug=True):
        """
        Starts the Flask-SocketIO server and runs it on the specified host and port.

        Args:
            host (str): The host address where the server will run. Default is "127.0.0.1".
            port (int): The port number where the server will be accessible. Default is 8085.
            debug (bool): Whether to run the server in debug mode. Default is True.
        """
        self.socketio.run(self.app, host=host, port=port, debug=debug)
