import adafruit_vl53l1x
import board
import digitalio

i2c = board.I2C()

xshut = [
    digitalio.DigitalInOut(board.D23),
    digitalio.DigitalInOut(board.D24),
    digitalio.DigitalInOut(board.D25),
    digitalio.DigitalInOut(board.D16),
]

vl53l1x = []


def initialize_sensors():
    for shutdown_pin in xshut:
        shutdown_pin.switch_to_output(value=False)

    for pin_number, shutdown_pin in enumerate(xshut):
        shutdown_pin.value = True
        sensor_i2c = adafruit_vl53l1x.VL53L1X(i2c)
        vl53l1x.append(sensor_i2c)
        if pin_number < len(xshut) - 1:
            sensor_i2c.set_address(pin_number + 0x30)

    for sensor in vl53l1x:
        sensor.distance_mode = 2
        sensor.timing_budget = 100
        sensor.start_ranging()


def get_distances():
    distances = []
    for sensor_number, sensor in enumerate(vl53l1x):
        if sensor.data_ready:
            distances.append(sensor.distance)
            sensor.clear_interrupt()
        return distances
