import irsdk
import time

class State:
    ir_connected = False
    last_speed_tick = -1

class IRTelemetry:
    def __init__(self, socketio):
        """
        Initialize the IRTelemetry class with an IRSDK instance and a SocketIO instance.
        """
        self.ir = irsdk.IRSDK()
        self.state = State()
        self.socketio = socketio  # Accept SocketIO instance

    def check_iracing(self):
        """
        Check the connection status with iRacing.
        Connect if not already connected, and disconnect if the connection is lost.
        """
        if self.state.ir_connected and not (self.ir.is_initialized and self.ir.is_connected):
            self.state.ir_connected = False
            self.ir.shutdown()
            print('irsdk disconnected')
        elif not self.state.ir_connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
            self.state.ir_connected = True
            print('irsdk connected')

    def retrieve_data(self):
        """
        Retrieve telemetry data from iRacing and emit it through SocketIO.
        """
        self.ir.freeze_var_buffer_latest()
        
        speed = self.ir['Speed'] * 3.6  # Convert speed to km/h
        steering_wheel_angle = self.ir['SteeringWheelAngle']
        brake = self.ir['Brake']
        throttle = self.ir['Throttle']
        clutch = 1 - self.ir['Clutch']  # Invert clutch value
        gear = self.ir['Gear']
        car_left_right = self.ir['CarLeftRight']
        car_dist_ahead = self.ir['CarDistAhead']
        car_dist_behind = self.ir['CarDistBehind']

        self.socketio.emit('telemetry_update', {
            'speed': speed,
            'steering_wheel_angle': steering_wheel_angle,
            'brake': brake,
            'throttle': throttle,
            'clutch': clutch,
            'gear': gear,
            'car_left_right': car_left_right,
            'car_dist_ahead': car_dist_ahead,
            'car_dist_behind': car_dist_behind
        })
