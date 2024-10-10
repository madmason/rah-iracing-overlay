import threading
from ir_webapp import socketio, app, telemetry

def start_telemetry():
    telemetry.run()

if __name__ == '__main__':
    telemetry_thread = threading.Thread(target=start_telemetry)
    telemetry_thread.start()

    print('Starting server...')
    socketio.run(app, host='127.0.0.1', port=8080)
