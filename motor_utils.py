import time
from threading import Thread
import RPi.GPIO as GPIO

# Pin definitions
motor_1_pin = 17
motor_2_pin = 27
motor_3_pin = 22
motor_4_pin = 5
motor_5_pin = 6
motor_6_pin = 13
motor_7_pin = 26

all_motors = [motor_1_pin, motor_2_pin, motor_3_pin,
              motor_4_pin, motor_5_pin, motor_6_pin, motor_7_pin]

motor_group_dict = {
    'motors_obstacle_high': [motor_1_pin, motor_2_pin],
    'motors_obstacle_mid': [motor_3_pin, motor_4_pin],
    'motors_obstacle_low': [motor_5_pin, motor_6_pin],
    'motors_obstacle_back': [motor_7_pin],
    'motors_obstacle_left': [motor_1_pin, motor_3_pin, motor_5_pin],
    'motors_obstacle_right': [motor_2_pin, motor_4_pin, motor_6_pin],
}

# GPIO active states
ON_STATE = GPIO.HIGH
OFF_STATE = GPIO.LOW

# Motor current state
current_motor_state = {
    motor_1_pin: [OFF_STATE, 'none'],
    motor_2_pin: [OFF_STATE, 'none'],
    motor_3_pin: [OFF_STATE, 'none'],
    motor_4_pin: [OFF_STATE, 'none'],
    motor_5_pin: [OFF_STATE, 'none'],
    motor_6_pin: [OFF_STATE, 'none'],
    motor_7_pin: [OFF_STATE, 'none']
}

# Motor speed pulses (in seconds)
pulse_speed = {
    'none': 0.2,
    'far': 2,
    'close': 1,
    'danger': 0.2,
}


def initialize_motors():
    GPIO.setwarnings(False)
    try:
        # GPIO.setmode(GPIO.BOARD)

        for motor in all_motors:
            GPIO.setup(motor, GPIO.OUT)
            motor_thread = Thread(target=pulse_motor, args=(motor, ))
            motor_thread.start()

    except KeyboardInterrupt:
        GPIO.cleanup()


def test_motors():
    for motor, state in current_motor_state.items():
        try:
            GPIO.output(motor, ON_STATE)
            time.sleep(1)
            GPIO.output(motor, OFF_STATE)
        except KeyboardInterrupt:
            GPIO.cleanup()


def turn_off_motors():
    try:
        for motor in all_motors:
            GPIO.output(motor, OFF_STATE)
    except KeyboardInterrupt:
        GPIO.cleanup()


def pulse_motor(motor):
    while True:
        global current_motor_state
        state = current_motor_state[motor]
        try:
            GPIO.output(motor, state[0])
            time.sleep(1)
            GPIO.output(motor, OFF_STATE)
            time.sleep(pulse_speed[state[1]])
        except KeyboardInterrupt:
            GPIO.cleanup()


def update_motors(obstacle_location: str, distance: str):
    global restart
    for motor in motor_group_dict[obstacle_location]:
        if current_motor_state[motor][1] == distance:
            continue
        state = OFF_STATE if distance == 'none' else ON_STATE
        current_motor_state[motor] = [state, distance]
        # motor_thread = Thread(target=pulse_motor, args=(motor, ))
        # motor_thread.start()
