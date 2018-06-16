#This script acts as the timer for the balancing machine, so when the balancing machine is activated, it counts down from 8 seconds
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

while 1:
    #Gets the parameter to check whether the balancing machine has a rotor in it
    bal_filled = RDK.getParam('bal_filled')

    #If balancing machine has a rotor in it, the internal timer is set to 8
    if bal_filled == 1:
        bal_time = 8

        #After the internal timer is set to 8, it counts down 1 every second until zero and sets the station parameter
        while bal_time > 0:
            sleep(1)
            bal_time -= 1
            RDK.setParam('bal_time', bal_time)

        #Waits until the machine is no longer filled before waiting for it to be filled again
        while bal_filled == 1:
            sleep(0.2)
            bal_filled = RDK.getParam('bal_filled')

    sleep(0.2) #Waits 0.2 seconds before checking again
