import ShellyPy

# try connecting to the Shelly device under that ip
device = ShellyPy.Shelly("192.168.68.121")
# WILL throw an exception if the device is not reachable, gives a bad response or requires a login

deviceMeter = device.meter(0)   #request meter information
print(deviceMeter['power'])     #print power information
print(deviceMeter['overpower']) #print overpower information
print(deviceMeter['is_valid'])  #print is_valid information
print(deviceMeter['timestamp']) #print timestamp information
print(deviceMeter['counters'])  #print counters information
print(deviceMeter['total'])     #print total information

device.update()
print(device)

