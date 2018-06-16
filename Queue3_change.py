#Identical to Queue1_change, but for queue table 3
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

q3_table = RDK.Item('Queue 3 table')

def change_table():
    q3_rotors = q3_table.Childs()
    for i in range(16):
        q3_rotors[i].Delete()


while 1:
    q3 = RDK.getParam('q3')
    if q3 == 16:
        mbox('Empty q3')
        change_table()
        RDK.setParam('q3', 0)

    sleep(0.5)
