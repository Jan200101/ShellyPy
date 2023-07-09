import ShellyPy

device = ShellyPy.api.Device.connect("192.0.0.20")

# open all rollers
device.rollers.open()

# close all rollers
device.rollers.close()

# stop all rollers
device.rollers.stop()

# set roller 1 position to 50% (requires calibration)
device.rollers[1].pos = 50 # 50%

# calibrate roller 1 (will find new min and max position)
device.rollers[1].calibrate()
