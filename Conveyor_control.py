#This script will add a rotor at a time to the conveyor belt, if the conveyor belt doesn't have one
#This can happen either automatically or manually via a prompt box
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

conveyor = RDK.Item('Conveyor')

#Prompt for whether the adding of 
manual_use = mbox('Do you wish for manual or automatic supply of rotors? 0 for manual', entry = True)
manual_use_number = int(manual_use)

#r'C:\Users\galas\Desktop\rob2\P2\rotor1forben.STL'

#This functions adds the rotor the conveyor belt and changes conv to 1 in the station parameters
def add_rotor():
    #Adds the object from the file rotor.stl to the workspace, and sets it parent to be the conveyor
    rotor = RDK.AddFile('/home/benjamin/Documents/RoboDK/station_objects/rotor.stl', conveyor) 
    rotor.setVisible(True, False) #Hides the object frame in the simulation
    rotor_pos_array = [80.886, 9.35, 45, 0, 1.571, 0] #Sets rotor position and euler angles
    rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array) #Converts those into a pose
    rotor.setPose(rotor_pose)
    RDK.setParam('conv', 1)

#This code will be run if manually adding rotors has been choosen
if manual_use_number == 0:
    while 1:
        state = RDK.getParam('conv') #Gets the parameter that describes whether there is a rotor on conveyor or not
        if state == 0: #Checks if there is no rotor on the conveyor 
            sleep(1) #If there is no rotor, sleep for a second
            mbox('Push for rotor') #Then make a prompt for adding a rotor
            add_rotor() #Then add a rotor
        else:
            sleep(0.5) #If there is a rotor, sleep for half a second before checking again
else:
    while 1: #The same thing happens here, except it kips the prompt
        state = RDK.getParam('conv')
        if state == 0: 
            sleep(1)
            add_rotor()
        else:
            sleep(0.5)
