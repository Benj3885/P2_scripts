#Identical to Bal_timer, but for the engraving machine
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

while 1:
    eng_filled = RDK.getParam('eng_filled')
    
    if eng_filled == 1:
        eng_time = 8

        while eng_time > 0:
            sleep(1)
            eng_time -= 1
            RDK.setParam('eng_time', eng_time)

        while eng_filled == 1:
            sleep(0.2)
            eng_filled = RDK.getParam('eng_filled')

    sleep(0.2)
