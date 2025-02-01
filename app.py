import time

import flask
from flask import Flask, render_template, Response, request, jsonify
import logging
import gevent
import cv2
from task1_opencv_control.modules.opencv_controller import OpenCVController
from task2_motor_control.modules.motor_controller import MotorController
from task3_sensor_control.modules.sensor_controller import SensorController

app = Flask(__name__)
motor_controller = MotorController()
opencv_controller = OpenCVController()
sensor_controller = SensorController()

start_time = 0
@app.route('/')
def index():
    """Server view to access the app and display the index template."""
    return render_template('index.html')


# Video Streaming Generator
BOUNDARY = 'frame'
ENCAPSULATION_BOUNDARY = b'\r\n--' + BOUNDARY.encode() + b'\r\n'
MIME_HEADER = b'Content-Type: image/jpeg\r\n\r\n'


def get_frames():
    while True:
        frame_gen = opencv_controller.process_frame()

        ret, buffer = cv2.imencode('.jpg', frame_gen)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
#       time.sleep(0.5)


@app.route('/video_feed')
def video_feed():
    """Server view to access the app and display the index template."""
    return Response(get_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_digit_from_opencv')
def get_digit_from_opencv():
    """Server view to determine the current digit zone using
        the opencv_controller.
    """
    return jsonify(opencv_controller.get_current_shape())


@app.route('/start_motor')
def start_motor():
    global start_time
    start_time = time.time()
    """Server view to start the motor."""
    motor_controller.start_motor()
    # ...
    return {'success': True}


@app.route('/stop_motor')
def stop_motor():
    """Server view to stop the motor."""
    global start_time
    motor_controller.stop_motor()
    if(start_time > 0):
        total_time = time.time() - start_time
        total_time=round(total_time, 2)
        start_time = 0
        return jsonify(total_time)
    else :
        total_time = 0
        return jsonify(total_time)


@app.route('/motor_status')
def motor_status():
    """Server view to get status of the motor (working or not working)."""
    # ...
    print(motor_controller.is_working())
    return jsonify(motor_controller.is_working())


@app.route('/get_distance')
def get_distance():
    """Server view to calculate the current distance using
        the sensor_controller.
    """
    sensor_controller.track_rod()
    return jsonify(sensor_controller.get_distance())
    # ...
   # return {'success': True}


@app.route('/get_digit_from_distance')
def get_digit_from_distance():
    """Server view to determine the current digit zone using
        the sensor_controller.
    """
    return jsonify(sensor_controller. get_shape_from_distance())
    # ...
    #return {'success': True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
