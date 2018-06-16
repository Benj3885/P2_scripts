from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
import socket
RDK = Robolink()

#Parameters to connect to the robot is being set
HOST = "169.254.42.105" #robot ip
PORT = 30002 #port to connect to

# robot and tool object is being set
robot = RDK.Item('Select a robot', ITEM_TYPE_ROBOT)
tool = RDK.Item('Gripper')

RDK.setSimulationSpeed(1) #Simulation speed is being set to real time

#Opening the gripper before moving the robot
#robot.Disconnect() #Disconnecting from the robot
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket object is being created
#s.connect((HOST, PORT)) #Connecting to robot through socket
#Setting commands to send to the robot
#a = "set_tool_digital_out(0, False)"
#b = "\n"
#s.send(a.encode() + b.encode()) #Sending the encoded commands
#s.close() #Closing the connection to the robot through the socket
#robot.ConnectSafe(HOST, 100, 0.1) #Reconnecting to the robot

robot.setSpeed(1500, 1500, 2000, 180) #Setting the speed of the robot

#Getting objects, targets and reference frames from the workstation
conveyor = RDK.Item('Conveyor')
balancing_machine = RDK.Item('Balancing machine')
leaking_test_machine = RDK.Item('Leaking test machine')
engraving_machine = RDK.Item('Engraving machine')

drawer_closed = RDK.Item('Drawer closed')
drawer_open = RDK.Item('Drawer open')
drawer_open_app = RDK.Item('Drawer open app')
drawer_drop_app = RDK.Item('Drawer drop app')
drawer_drop = RDK.Item('Drawer drop')
drawer_pick = RDK.Item('Drawer pick')
drawer_pick_app = RDK.Item('Drawer pick app')
app_app = RDK.Item('App-app')
drawer = RDK.Item('Drawer')

leak_drop = [RDK.Item('Leaking drop 1'), RDK.Item('Leaking drop 2')]
leak_drop_app = [RDK.Item('Leaking drop 1 app'), RDK.Item('Leaking drop 2 app')]
leak_app = RDK.Item('Leak app')
lt_param = ['lt1', 'lt2']
trash = RDK.Item('Trash')
trash_obj = RDK.Item('Trash obj')

engraving_drop = RDK.Item('Engraving drop')
engraving_drop_app1 = RDK.Item('Engraving drop app 1')
engraving_drop_app2 = RDK.Item('Engraving drop app 2')

conveyor_drop_app = RDK.Item('Conveyor drop app')
conveyor_drop = RDK.Item('Conveyor drop')

queue_table = [RDK.Item('Queue 1 table'), RDK.Item('Queue 2 table'), RDK.Item('Queue 3 table')]
queue = [RDK.Item('Queue 1'), RDK.Item('Queue 2'), RDK.Item('Output trolley')]
queue_drop = [RDK.Item('Queue 1 drop app'), RDK.Item('Queue 2 drop app'), RDK.Item('Queue 3 drop app')]

#Function that closes the gripper and attaches nearest item to tool in RoboDK
def close_gripper():
    #robot.Disconnect()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))
    #a = "set_tool_digital_out(0, True)"
    #b = "\n"
    #s.send(a.encode() + b.encode())
    #s.close()
    #robot.ConnectSafe(HOST, 100, 0.1)
    
    tool.AttachClosest()
    robot.setSpeed(1500, 1500, 2000, 180) #Sets speed back to earlier value due to disconnecting resetting it

#Function that opens the gripper and detaches item from gripper to parent parameter
def open_gripper(parent):
    #robot.Disconnect()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))
    #a = "set_tool_digital_out(0, False)"
    #b = "\n"
    #s.send(a.encode() + b.encode())
    #s.close()
    #robot.ConnectSafe(HOST, 100, 0.1)
    
    tool.DetachAll(parent)
    robot.setSpeed(1500, 1500, 2000, 180) #Sets speed back to earlier value due to disconnecting resetting it

#Function that takes table (0, 1 or 2), dropping (0 or 1) and number (number of rotors on table)
#It uses the three parameters to set the reference frame of the table and to calculate the target appropiate for table and number of rotors
#It returns this target, which can be used with a MoveJ or MoveL command
def queue_target(table, dropping, number):
    target = Mat(queue_drop[table].Pose())
    target_pos = target.Pos()

    robot.setPoseFrame(queue[table])

    row = number % 4
    col = number // 4
    
    target_pos[0] = target_pos[0] + (0 - col) * 90
    target_pos[1] = target_pos[1] + (0 - row) * 90
    target_pos[2] = target_pos[2] - dropping * 200

    target.setPos(target_pos)

    return target

#Makes the robot move the rotor from the conveyor to the balancing machine
def conveyor_to_drawer():
    robot.setPoseFrame(conveyor)
    robot.MoveL(conveyor_drop)
    close_gripper()
    RDK.setParam('conv', 0)
    robot.MoveL(conveyor_drop_app)
    robot.setPoseFrame(balancing_machine)
    robot.MoveJ(drawer_drop_app)
    robot.MoveL(drawer_drop)
    open_gripper(drawer)
    robot.MoveL(drawer_drop_app)
    robot.MoveL(app_app)
    robot.MoveJ(drawer_open_app)

#Makes the robot open the balancing machine drawer
def balance_drawer_open():
    robot.setPoseFrame(balancing_machine)
    robot.MoveJ(drawer_open)
    robot.MoveL(drawer_closed)
    close_gripper()
    robot.MoveL(drawer_open)
    open_gripper(balancing_machine)
    robot.MoveL(drawer_open_app)

#Makes the robot close the balancing machine drawer
def balance_drawer_close():
    robot.setPoseFrame(balancing_machine)
    robot.MoveL(drawer_open_app)
    robot.MoveL(drawer_open)
    close_gripper()
    robot.MoveL(drawer_closed)
    open_gripper(balancing_machine)
    robot.MoveL(drawer_open)

#Makes the robot move the rotor from the balancing machine to the queue table 1
def drawer_pick_rotor():
    balance_drawer_open()
    robot.setPoseFrame(balancing_machine)
    robot.MoveL(app_app)
    robot.MoveJ(drawer_pick_app)
    robot.MoveL(drawer_pick)
    close_gripper()
    robot.MoveL(drawer_pick_app)
    RDK.setParam('bal_filled', 0)
    q1 = RDK.getParam('q1')
    robot.MoveL(queue_target(0, 0, q1))
    robot.MoveL(queue_target(0, 1, q1))
    open_gripper(queue_table[0])
    robot.MoveL(queue_target(0, 0, q1))
    q1 += 1
    RDK.setParam('q1', q1)
    
#Makes the robot open drawer, move rotor from conveyor to balancing machine and closes drawer
def balance_add_rotor():
    balance_drawer_open()
    robot.MoveL(conveyor_drop_app)
    conveyor_to_drawer()
    balance_drawer_close()
    RDK.setParam('bal_filled', 1)

#Open drawer, moves rotor from balancing machine to queue table 1, moves rotor from conveyor to balancing machine
def replace_balance_rotor():
    drawer_pick_rotor()
    robot.MoveJ(conveyor_drop_app)
    conveyor_to_drawer()
    balance_drawer_close()
    RDK.setParam('bal_filled', 1)

#Moves rotor 0 or 1 (rot_number) from leak testing machine to queue table 2
def leak_to_queue2(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    q2 = RDK.getParam('q2')
    robot.MoveL(queue_target(1, 0, q2))
    robot.MoveL(queue_target(1, 1, q2))
    open_gripper(queue_table[1])
    robot.MoveL(queue_target(1, 0, q2))
    q2 += 1
    RDK.setParam('q2', q2)

#Moves rotor 0 or 1 (rot_number) from leak testing machine to the engraving machine
def leak_to_engraving(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop)
    open_gripper(engraving_machine)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 1)

#Moves rotor 0 or 1 (rot_number) from leak testing machine to trash can
def leak_to_trash(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    #robot.setRounding(0)
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    #robot.setRounding(50)
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    robot.MoveJ(trash)
    open_gripper(trash_obj)
    defect_rotor = trash_obj.Childs()
    defect_rotor[0].Delete()

#Moves rotor from engraving machine to output trolley
def engraving_to_output():
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop)
    close_gripper()
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 0)
    q3 = RDK.getParam('q3')
    robot.MoveJ(queue_target(2, 0, q3))
    robot.MoveL(queue_target(2, 1, q3))
    open_gripper(queue_table[2])
    robot.MoveL(queue_target(2, 0, q3))
    q3 += 1
    RDK.setParam('q3', q3)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)

#Moves rotor from queue2 to engraving machine
def queue2_to_engraving():
    q2 = RDK.getParam('q2')
    q2 -= 1
    robot.MoveJ(queue_target(1, 0, q2))
    robot.MoveL(queue_target(1, 1, q2 ))
    close_gripper()
    robot.MoveL(queue_target(1, 0, q2))
    RDK.setParam('q2', q2)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop)
    open_gripper(engraving_machine)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 1)


#Side is defined so that the robot will go to a point when moving from one side of the workspace to the other
#This is done in order to avoid collision with the leaking test machine
side = 1

while 1: #Loop with the ddecision-making
    #Starting out by getting all the station parameters
    bal_filled = RDK.getParam('bal_filled')
    conv = RDK.getParam('conv')
    q1 = RDK.getParam('q1')
    bal_time = RDK.getParam('bal_time')

    new_round = False #Used to restart loops from inside for loops where continue doesn't work
    lt = [RDK.getParam('lt1'), RDK.getParam('lt2')]
    eng_filled = RDK.getParam('eng_filled')
    eng_time = RDK.getParam('eng_time')
    q2 = RDK.getParam('q2')
    q3 = RDK.getParam('q3')    

    #Adds a rotor to balancing machine if balancing machine is empty and there is a rotor on conveyor
    if conv == 1 and bal_filled == 0:
        if side == 2: #If on second side and moving to first side, moves to target leak_app
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        balance_add_rotor()
        RDK.setParam('bal_time', 8) #Done so that the next loop doesn't have a false positive in case bal_timer doesn't start the timer in time
        continue #Starts a new round in the while loop

    #Opens drawer, moves rotor from balancing machine to queue1 and from conveyor to drawer
    #Is true when there is rotor on conveyor, rotor in balancing machine drawer, machine is done and there is room on queue table 1
    if conv == 1 and bal_filled == 1 and bal_time == 0 and q1 < 16:
        if side == 2:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        replace_balance_rotor()
        RDK.setParam('bal_filled', 1)
        RDK.setParam('bal_time', 8)
        continue

    #For loop checking if the rotors in the engraving machine are ready for the engraving machine
    for i in range(2):
        if lt[i] != 1: #If there isn't a rotor, or it should be thrown out, looks at next rotor or breaks the for loop
            continue

        #If there isn't a rotor in the engraving machine, then the rotor will be moved there from the leak testing machine
        if eng_filled == 0:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_engraving(i)
            RDK.setParam('eng_time', 8)
            new_round = True #new_round is set to true to start a new iteration in the while loop
            break #Breaks the for loop

        #If there is a rotot in the engraving machine, the machine is done and there is room on the output
        #Moves rotor from engraving machine to output trolley and from leak testing machine to engraving machine
        if eng_filled == 1 and eng_time == 0 and q3 < 16:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            engraving_to_output()
            leak_to_engraving(i)
            RDK.setParam('eng_time', 8)
            new_round = True
            break

    if new_round:
        continue

    #If there is a rotor in queue table 2, and the engraving machine is empty, moves a rotor from queue table 2 to the engraving machine
    if q2 != 0 and eng_filled == 0:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        queue2_to_engraving()
        RDK.setParam('eng_time', 8)
        continue
    
    #If there is a rotor in queue table 2, and the engraving machine isn't empty, and the engraving machine is done
    #moves a rotor from queue table 2 to the engraving machine
    if q2 != 0 and eng_filled == 1 and eng_time == 0 and q3 < 16:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        engraving_to_output()
        robot.setPoseFrame(engraving_machine)
        robot.MoveL(engraving_drop_app2)

        lt = [RDK.getParam('lt1'), RDK.getParam('lt2')]

        skip = False #Used for stopping the moving of rotor from queue table 2 to engraving machine if next if-statement in the next for loop is true

        #Checks if a rotor has become available in the leak testing machine while the rotor from the negraving machine was moved to output trolley
        #If so, one of those are used rather than a rotor from queue table 2
        for i in range(2): 
            if lt[i] == 1:
                leak_to_engraving(i)
                RDK.setParam('eng_time', 8)
                skip == True
                break

        if skip:
            continue
        
        queue2_to_engraving()
        RDK.setParam('eng_time', 8)
        continue

    #Checks if a rotor from the leak testing machine should be moved to trash or queue table 2
    for i in range(2):
        #Checks for queue table 2
        if lt[i] == 1 and q2 < 16:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_queue2(i)
            lt[i] = 0
            new_round = True
            break

        #Checks for trash
        if lt[i] == 2:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_trash(i)
            lt[i] = 0
            new_round = True
            break
            
    if new_round:
        continue
    
    #If there is a rotor in the balancing machine, there is room on queue table 1 and the balancing machine is done,
    #moves the rotor from the balancing machine to queue table 1
    if bal_filled == 1 and q1 < 16 and bal_time == 0:
        if side == 2:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        drawer_pick_rotor()

        #Checks if a new rotor has come one the conveyor belt, in which case that one is added to the balancing machine
        conv = RDK.getParam('conv')

        if conv == 1:
            balance_add_rotor()
            RDK.setParam('bal_time', 8)
        
        balance_drawer_close()
        continue

    #If there is a rotor in the engraving machine, the machine is done and ther eis room for a rotor on the output trolley
    #move the rotor from the engraving machine to the output trolley
    if eng_filled == 1 and eng_time == 0 and q3 < 16:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        engraving_to_output()
        continue


    
    
