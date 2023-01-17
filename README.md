# ShellyPy
not to be confused with [pyShelly](https://github.com/StyraHem/pyShelly)  
Python 2 and 3 Wrapper around the Shelly HTTP api


## why
other packages like [pyShelly](https://github.com/StyraHem/pyShelly) only support CoAP or MSQT, neither I am comfortable with using in personal projects


## examples
#### relay
a simple working example for the Shelly 1 that turns a relay on 
```python
import ShellyPy

device = ShellyPy.Shelly("192.168.0.5")

device.relay(0, turn=True)
```
[examples/toggle_relay.py](examples/toggle_relay.py)

#### monitor
a simple working example for the Shelly 1 that request monitor information 
```python
import ShellyPy

device = ShellyPy.Shelly("192.168.68.121")

deviceMeter = device.meter(0)   #request meter information
print(deviceMeter['power'])     #print power information
print(deviceMeter['total'])     #print total information
```
other examples are available as well [examples/meter.py](examples/meter.py)

## devices
#### supported
- Shelly1
- Shelly1PM
- Shelly2
- Shelly2.5
- Shelly4Pro (untested)
- Shelly Plug (untested)
- Shelly PlugS (untested)
- Shelly Bulb (untested)
- Shelly H&T (untested)
- Shelly Smoke (untested)
- Shelly EM (untested)
- Shelly flood (untested)

#### unsupported
- Shelly Sense (documentation is inaccurate, incomplete)
- Shelly RGBW (documentation is incomplete)

## applicability
this wrapper is best used in closed networks where other solutions are either not an option or not desired  
give your shelly devices static IP adresses for best results


## license
this project is licensed under the [MIT License](LICENSE)  
feel free to do whatever you want with it
