import sys
import pprint
import uuid
import time
import os, json
import ibmiotf.device
from uuid import getnode as get_mac
import grovepi
devicecli = None

def myCommandCallback(event):
        print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

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

