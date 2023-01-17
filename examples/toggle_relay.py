import ShellyPy

# try connecting to the Shelly device under that ip
device = ShellyPy.Shelly("192.168.0.5")
# WILL throw an exception if the device is not reachable, gives a bad response or requires a login

device.relay(0, turn=True) # turn the relay at index 0 on
device.relay(0, turn=False) # same as above but turn it off
device.relay(0, turn=True, delay=3) # turn the relay 0 on for 3 seconds then off
# most shelly devices only have 1 or 2 relays
