##########################################################3########################################
#       Bauman hackathon python code example 
#
#       This module use ibmiot.device library to send MQTT events to Bluemix IoT application
#       (on NodeRED for ex.) and receive commands in MQTT messages back from Bluemix.
#       This code using /home/pi/iot/device.cfg configuration file
#       to get device credentials. 
#       Configuration file format:
#
#       [device]
#       type=
#       org=
#       id=
#       auth-method=token
#       auth-token=
#
#       This information can be taken from IoT Foundation service after adding device.
#       You can use simple NodeRed flow to test this code: 
#
#       [{"id":"2d75d543.dad442","type":"ibmiot","z":"c238f5f0.b89fa8","name":"Pi"},{"id":"95d6bda2.ce688","type":"ibmiot in","z":"c238f5f0.b89fa8","authentication":"apiKey","apiKey":"2d75d543.dad442","inputType":"evt","deviceId":"9094E436E58E","applicationId":"","deviceType":"+","eventType":"+","commandType":"","format":"json","name":"IBM IoT App In","service":"registered","allDevices":false,"allApplications":false,"allDeviceTypes":true,"allEvents":true,"allCommands":false,"allFormats":false,"x":163.88333129882812,"y":771.13330078125,"wires":[["fcb6ba8b.0a7b28"]]},{"id":"fcb6ba8b.0a7b28","type":"function","z":"c238f5f0.b89fa8","name":"","func":"inputs = msg.payload;\nresult = inputs.INPUT1 && inputs.INPUT2;\nmsg.payload = {'result' : result};\nmsg.eventOrCommandType = \"signal\";\nreturn msg;","outputs":1,"noerr":0,"x":380.88336181640625,"y":771.63330078125,"wires":[["68e73082.9c3c18"]]},{"id":"68e73082.9c3c18","type":"json","z":"c238f5f0.b89fa8","name":"","x":582.0000305175781,"y":772.6000061035156,"wires":[["afbfaa7b.2ea348"]]},{"id":"afbfaa7b.2ea348","type":"ibmiot out","z":"c238f5f0.b89fa8","authentication":"apiKey","apiKey":"2d75d543.dad442","outputType":"cmd","deviceId":"9094E436E58E","deviceType":"Pi","eventCommandType":"signal","format":"json","data":"{'result':0}","name":"IBM IoT","service":"registered","x":785.88330078125,"y":773.63330078125,"wires":[]}]
#
#	Do not forget to insert apiKey and apiToken for you instance of IoT Foundation 
#	(Internet of Things Platform -> Show Credentials ->)
#
#      	Other useful links:
#
#       https://github.com/ibm-messaging/iot-python/tree/master/samples
#       https://docs.internetofthings.ibmcloud.com/devices/libraries/python.html
#
#
#
###################################################################################################
import RPi.GPIO as GPIO
import time
import os, json
import ibmiotf.device
import uuid
from uuid import getnode as get_mac


GPIO.setmode(GPIO.BCM)
#INPUT 1
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#INPUT 2
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#OUTPUT = (INPUT 1 AND INPUT 2)
GPIO.setup(3, GPIO.OUT)

client = None

#Define command tracer 

def myCommandCallback(cmd):

    if cmd.command == "signal":
        result = cmd.data['result']
        print ("Command received, result = %d" %result)
        if result == 1:
            GPIO.output(3, True)
        elif result == 0:
            GPIO.output(3, False)
# Initialize the device client.
try:

    #Parse config file
    options = ibmiotf.device.ParseConfigFile("/home/pi/diplom/device.cfg")

    #Connect with Bluemix IoT 
    client = ibmiotf.device.Client(options)
    client.connect()

    #Initialize callback

    client.commandCallback = myCommandCallback

    while True:

        #Send Input 1 and Input 2
        myData = {'INPUT1' : GPIO.input(7), 'INPUT2' : GPIO.input(11)}
        client.publishEvent("data", "json", myData)
        time.sleep(1.0)

except ibmiotf.ConnectionException  as e:
    print e



