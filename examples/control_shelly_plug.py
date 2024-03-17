#!/usr/bin/env python
# helper script to query, turn on and off a Shelly Plug (tested with Shelly Plug US / Gen 2)
# and print status

# requires: pip3 install shellypy

# script configuration
device_ip = "192.168.1.99"

# start of code

import ShellyPy
import sys
import argparse
import time


try:
        device = ShellyPy.Shelly(device_ip, login = {'username' : 'admin', 'password' : 'some_password'} )

        device.update()
        print("Device Found:", device)
        # print(device.status())
        # print(device.settings())

        switch_status = device.relay(0)
        if switch_status['output']:
                load_state = 'ON'
        else: load_state = 'OFF'
        load_power = switch_status['apower']
        load_voltage = switch_status['voltage']
        load_current = switch_status['current']
        #  print("Switch Status: ", device.relay(0))
        # returns a dict current full state:
        #  output: true / false (on / offl
        #  voltage, current, apower, etc
except:
        print("Issue finding/initializing device - aborting script")
        sys.exit()



# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-1",
    "--turn-on",
    help="turn on the switch in the device",
    action="store_true",
)
parser.add_argument(
    "-0",
    "--turn-off",
    help="turn off the switch in the device",
    action="store_true",
)

parser.add_argument(
    "-s",
    "--status",
    help="print status of device",
    action="store_true",
)


args = parser.parse_args()
if not len(sys.argv) > 1:
    args.status = True  
    # if no arguments, then print device status


if args.status:      
        print('Device Status: ')
        print('  Load State:', load_state)
        print('  Load Power:', load_power, 'W')
        print('  Load Voltage:', load_voltage, 'V')
        print('  Load Current:', load_current, 'A')
if args.turn_on:
        #Turn on
        device.relay(0, turn=True)
        print('The Load state is now ON')
if args.turn_off:
        #Turn off
        device.relay(0, turn=False)
        print('The Load state is now OFF')

