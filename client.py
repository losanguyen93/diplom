import sys
import RPi.GPIO as GPIO
import pprint
import uuid
import time
import os, json
import ibmiotf.device
from uuid import getnode as get_mac
import grovepi
devicecli = None

#Define command tracer
def myCommandCallback(cmd):
       if cmd.command == 'signal':
        result = cmd.data['result']
        print ("Command received, result = %d" %result)

# Initialize the device client.
sensor = 0
try:

    #Parse config file
    options = ibmiotf.device.ParseConfigFile("/home/pi/diplom/device.cfg")

    #Connect with Bluemix IoT
    devicecli = ibmiotf.device.Client(options)
    devicecli.connect()
    devicecli.commandCallback = myCommandCallback
    while True:
        try:
           temp = grovepi.temp(sensor,'1.1')
           print "ok temp=", temp
           myData={'temperature_sensor' : temp}
           devicecli.publishEvent("status", "json", myData)
           time.sleep(5)
        except KeyboardInterrupt:
           break
        except IOError:
           print "Error"

except ibmiotf.ConnectionException  as e:
    print e
