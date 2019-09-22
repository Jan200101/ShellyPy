import ShellyPy

device = ShellyPy.Shelly("192.168.0.5") # try connecting to the Shelly device under that ip

device.relay(0, turn=True) # turn the relay at index 0 on
device.relay(0, turn=False) # same as bove but turn it off
