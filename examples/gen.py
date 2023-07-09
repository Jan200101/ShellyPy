import ShellyPy

# Automatically detect device generation and return the right class
device = ShellyPy.api.Device.connect("192.0.0.20")

# Explicitly connect a Generation 1 Device
device_gen1 = ShellyPy.api.gen1.Device.connect("192.0.0.21")

# Explicitly connect a Generation 2 Device
device_gen2 = ShellyPy.api.gen2.Device.connect("192.0.0.22")
