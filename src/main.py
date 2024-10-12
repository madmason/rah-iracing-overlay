import threading
from ir_telemetry import IRTelemetry
from ir_webapp import IRWebApp

if __name__ == '__main__':
    web_app = IRWebApp()
    telemetry = IRTelemetry(web_app.socketio)
    telemetry_thread = threading.Thread(target=telemetry.run, daemon=True)
    telemetry_thread.start()
    web_app.run()
