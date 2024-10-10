import irsdk
import time
import json
from flask_socketio import SocketIO

class State:
    ir_connected = False
    last_speed_tick = -1

class IRTelemetry:
    def __init__(self, socketio):
        self.ir = irsdk.IRSDK()
        self.state = State()
        self.socketio = socketio

    def check_iracing(self):
        if self.state.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
            self.state.ir_connected = False
            self.ir.shutdown()
            print('irsdk disconnected')
        elif not self.state.ir_connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
            self.state.ir_connected = True
            print('irsdk connected')

    def retrieve_speed(self):
        self.ir.freeze_var_buffer_latest()
        speed = self.ir['Speed']
        if speed:
            self.socketio.emit('speed_update', {'speed': speed})

    def run(self):
        while True:
            self.check_iracing()
            if self.state.ir_connected:
                self.retrieve_speed()
            time.sleep(0.05)