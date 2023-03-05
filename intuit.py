import time
import sensor_utils as sensors
import motor_utils as motors

SENSOR_LIST = ['sensor_front']

sensor_motor_group_dict = {
    'sensor_front': 'motors_obstacle_high',
    'sensor_mid': 'motors_obstacle_mid',
    'sensor_low': 'motors_obstacle_low',
    'sensor_back': 'motors_obstacle_back',
    'sensor_left': 'motors_obstacle_left',
    'sensor_right': 'motors_obstacle_right'
}

def setup():
    motors.initialize_motors()
    sensors.initialize_sensors()

def walk():
    while True:
        distance = sensors.get_distances()
        sensor = SENSOR_LIST[0]
        if not distance or distance > 300:
            motors.update_motors(sensor_motor_group_dict[sensor], 'none')
        elif distance > 200 and distance <= 300:
            motors.update_motors(sensor_motor_group_dict[sensor], 'far')
        elif distance > 100 and distance <= 200:
            motors.update_motors(sensor_motor_group_dict[sensor], 'close')
        else:
            motors.update_motors(sensor_motor_group_dict[sensor], 'danger')
        time.sleep(0.1)

setup()
walk()

# motors.test_motors()
