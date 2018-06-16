#This script will create a prompt when queue table 1 is filled with rotors
#When clicking on the promt button, it will then delete all rotors from queue table 1 and reset parameter q1 to 0
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

#Gets the queue table 1 object from the workspace
q1_table = RDK.Item('Queue 1 table')

#Function that deletes the rotors from the queue table 1 object
def change_table():
    q1_rotors = q1_table.Childs()
    for i in range(16):
        q1_rotors[i].Delete()

#Loop that checks if table is filled
while 1:
    q1 = RDK.getParam('q1')
    if q1 == 16:
        mbox('Empty q1')
        change_table()
        RDK.setParam('q1', 0)

    sleep(0.5)
