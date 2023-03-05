import adafruit_vl53l1x
import board

i2c = board.I2C()

vl53 = adafruit_vl53l1x.VL53L1X(i2c)


def initialize_sensors():
    vl53.distance_mode = 2
    vl53.timing_budget = 100
    vl53.start_ranging()


def get_distances():
    if vl53.data_ready:
        distance = vl53.distance
        vl53.clear_interrupt()
        return distance
