import os 
import time 
import socket
import tkinter as tk 
from tkinter import messagebox
from math import radians, degrees, pi
import numpy as np
from robodk.robolink import *
from robodk.robomath import *

# Load RoboDK project from relative path
relative_path = "src/roboDK/Assistive_UR5e_Roc_Maite.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()
RDK.AddFile(absolute_path)

# Robot setup
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Target_1 = RDK.Item('Target 1')
Target_2 = RDK.Item('Target 2')
Target_3 = RDK.Item('Target 3')
Target_4 = RDK.Item('Target 4')
Target_5 = RDK.Item('Target 5')
Target_6 = RDK.Item('Target 6')
Target_7 = RDK.Item('Target 7')
Target_8 = RDK.Item('Target 8')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(100)

# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 4

# URScript commands
tg1_joints = list(np.radians(Target_1.Joints())[0])
tg2_joints = list(np.radians(Target_2.Joints())[0])
tg3_joints = list(np.radians(Target_3.Joints())[0])
tg4_joints = list(np.radians(Target_4.Joints())[0])
tg5_joints = list(np.radians(Target_5.Joints())[0])
tg6_joints = list(np.radians(Target_6.Joints())[0])
tg7_joints = list(np.radians(Target_7.Joints())[0])
tg8_joints = list(np.radians(Target_8.Joints())[0])

set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"
movej_target_1 = f"movej({tg1_joints},1.20000,0.75000,{timej},0.0000)"
movel_target_2 = f"movel({tg2_joints},{accel_mss},{speed_ms},{timel},0.0000)"
movel_target_4 = f"movel({tg4_joints},{accel_mss},{speed_ms},{timel},0.0000)"
movel_target_6 = f"movel({tg6_joints},{accel_mss},{speed_ms},{timel},0.0000)"
movec_taget_3 = f"movec({tg8_joints},{tg3_joints},{accel_mss},{speed_ms},{timel},0.0000)"
movec_target_5 = f"movec({tg7_joints},{tg5_joints},{accel_mss},{speed_ms},{timel},0.0000)"


# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())

# Wait for robot response
def receive_response(t):
    try:
        print("Waiting time:", t)
        time.sleep(t)
    except socket.error as e:
        print(f"Error receiving data: {e}")
        exit(1)


# Movements
def Init():
    print("Init")
    robot.MoveJ(Target_1, True)
    print("Init_target REACHED")
    if robot_is_connected:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movej_target_1)
        receive_response(timej)
    else:
        print("UR5e not connected. Simulation only.")


def Cleaning_table():
    print("Cleaning table")
    robot.setSpeed(100)
    robot.MoveL(Target_2, True)
    robot.MoveL(Target_4, True)
    robot.MoveC(Target_8, Target_3, True)
    robot.MoveL(Target_6, True)
    robot.MoveC(Target_7, Target_5, True)
    robot.MoveL(Target_4, True)
    robot.MoveC(Target_8, Target_3, True)
    robot.MoveL(Target_6, True)
    robot.MoveC(Target_7, Target_5, True)
    robot.MoveL(Target_2, True)
    robot.MoveL(Target_1, True)
    if robot_is_connected:
        print("Cleaning_table REAL UR5e")
        send_ur_script(set_tcp)
        receive_response(1)
        send_ur_script(movel_target_2)
        receive_response(timel)
        send_ur_script(movel_target_4)
        receive_response(timel)
        send_ur_script(movec_taget_3)
        receive_response(timel) # maybe change time
        send_ur_script(movel_target_6)
        receive_response(timel)
        send_ur_script(movec_target_5)
        receive_response(timel) # maybe change time
        send_ur_script(movel_target_4)
        receive_response(timel)
        send_ur_script(movec_taget_3)
        receive_response(timel) # maybe change time
        send_ur_script(movel_target_6)
        receive_response(timel)
        send_ur_script(movec_target_5)
        receive_response(timel) # maybe change time
        send_ur_script(movel_target_2)
        receive_response(timel)
        send_ur_script(movej_target_1)
        receive_response(timel)


# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Main function
def main():
    global robot_is_connected
    robot_is_connected = check_robot_port(ROBOT_IP, ROBOT_PORT)
    Init()
    Cleaning_table()
    if robot_is_connected:
        robot_socket.close()

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()
