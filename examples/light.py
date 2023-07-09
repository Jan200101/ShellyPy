import ShellyPy

device = ShellyPy.api.Device.connect("192.0.0.20")

# turn all lights off
device.lights.off()

# turn all lights on
device.lights.on()

# toggle all lights
device.lights.toggle()

# return light 0 on
device.lights[0].on()

# Set Brightness in percent
device.lights[0].brightness = 50 # 50%

# Set RGB colors (Gen 1 only)
device.lights[0].rgb = (255, 255, 255)

# Set RGBW colors (Gen 1 only)
device.lights[0].rgbw = (128, 128, 128, 0)

# Set only one color (Gen 1 only)
device.lights[0].red = 64
