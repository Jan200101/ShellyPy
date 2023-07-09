import ShellyPy

device = ShellyPy.api.Device.connect("192.0.0.20")

# turn all relays off
device.relays.off()

# turn all relays on
device.relays.on()

# toggle all relays
device.relays.toggle()

# return relay 0 on
device.relays[0].on()
