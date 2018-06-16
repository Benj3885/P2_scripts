#This script is in charge of adding rotors to the leaking test machine based on input from user prompt
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

sleep_time = 0 #Parameter for how long it takes suntil the rotors appear in the leaking test machine. Set to 0 for testing purposes

leaking_test_machine = RDK.Item('Leaking test machine')

#The position of the rotors in coordinates and euler angles set so that they fit the holders in the leaking test machine
rotor_pos_array1 = [346, 541, 245.5, 3.141593, 0, 0]
rotor_pos_array2 = [196, 541, 245.5, 3.141593, 0, 0]

#The function that gets input from user and converts it to an int
def get_input():
    rotor_states = mbox('Enter rotor states: 0 not existing, 1 for success, 2 for defect', entry = True)
    rotor_state_number = int(rotor_states)
    return rotor_state_number

while 1:
    #Sets to booleans to control
    done = False
    waiting = True

    while waiting: #This loop makes the program wait until there are no rotors in the leak testing machine
        rotor1_param = RDK.getParam('lt1')
        rotor2_param = RDK.getParam('lt2')

        if rotor1_param == 0 and rotor2_param == 0: #This if-statement is true if there are no rotors in the leaking test holders
            waiting = False #By changing waiting to false, the program will move to the next loop
        sleep(0.5)
    
    while not done: #This loop is responsible for getting a usable input from the user
        rotor_state_number = get_input() #Getting the input
        rot = [rotor_state_number // 10, rotor_state_number % 10] #Getting the state from the input

        if rot[0] < 3 and rot[0] >= 0 and rot[1] < 3 and rot[1] >= 0: #If the input is valid, then this if-statement will stop the loop
            done = True

    current_sleep_timer = sleep_time

    RDK.setParam('lt_time', sleep_time) #Sets the time left on the machine to sleep_time (0)
    while current_sleep_timer > 0: #Countdown loop that sets the station parameter to remaining time every second
        sleep(1)
        current_sleep_timer -= 1
        RDK.setParam('lt_time', current_sleep_timer)
    
    for i in range(2): #Sets the new station parameters for what rotors the leak testing machine is holding
        if i == 0:
            RDK.setParam('lt1', rot[i])
        else:
            RDK.setParam('lt2', rot[i])

        #r'C:\Users\galas\Desktop\rob2\P2\rotor1forben.STL'

        if rot[i] > 0: #If there is a rotor, then one is added in the workstation
            rotor = RDK.AddFile('/home/benjamin/Documents/RoboDK/station_objects/rotor.stl', leaking_test_machine) #Rotor is added from path and has parent leak_testing_machine
            rotor.setVisible(True, False) #Rotor frame is hidden
            rotor_pose = 0 # rotor_pose is declared outside if and else scope
            if i == 0: #The right rotor pose is selected
                rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array1)
            else:
                rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array2)
            rotor.setPose(rotor_pose) #Rotor pose it set

    


    
