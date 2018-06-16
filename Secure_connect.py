#This script will continuously reconnect to the robot in case connectSafe fails
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

#Connects to the robot
robot = RDK.Item('Select a robot', ITEM_TYPE_ROBOT)
robot.Connect()

#Connect to the robot every 0.1 second
while 1:
    robot.Connect()
    sleep(0.1)
