# This script is used to make two vx300s arm to perform a team-task
# 
# Note that this script may not work for every arm as it was designed for the wx250
# Make sure to adjust commanded joint positions and poses as necessary
#
# To get started, open a terminal and type 'roslaunch interbotix_xsarm_control xsarm_control.launch robot_model:=wx250'
# Then change to this directory and type 'python bartender.py  # python3 bartender.py if using ROS Noetic'

import math
import rospy
from interbotix_xs_modules.arm import InterbotixManipulatorXS
from threading import Thread
from time import sleep


def arm_1_pick_and_handover():
    # Initialize Arm 1 (e.g., vx300s model)
    arm_1 = InterbotixManipulatorXS(robot_model="vx300s", robot_name= "arm_1", moving_time=1.0, gripper_pressure=1.0, init_node=False)
    # Arm 1 picks up the object
    arm_1.arm.set_ee_pose_components(x=0.26, z=0.2)  # Move to above the object
    arm_1.arm.set_single_joint_position("waist", math.pi/2.0)
    rospy.sleep(1.0)
    arm_1.gripper.open()                            # Open gripper
    arm_1.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.15)   # Move down to pick up object on z-axis
    rospy.sleep(1.5)     
    arm_1.gripper.close()                 # Close gripper
    rospy.sleep(0.5) 
    arm_1.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.15)    # Lift object
    rospy.sleep(1.5)
    arm_1.gripper.open()
    rospy.sleep(1.0)
    arm_1.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.3) 
    rospy.sleep(1.0) 
    
    # Arm 1 moves to handover position
    arm_1.arm.set_ee_pose_components(x=-0.1, y=0, z=0.2)  # Move to handover position
    arm_1.arm.set_single_joint_position("waist", 0)

    arm_1.arm.go_to_sleep_pose()
    arm_1.gripper.close()

def arm_2_receive_and_move():
    # Initialize Arm 2 (e.g., vx300s model)
    arm_2 = InterbotixManipulatorXS(robot_model="vx300s", robot_name="arm_2", moving_time=1.0, gripper_pressure=1.0, init_node=False)
    
    # Arm 2 moves to handover position
    arm_2.arm.set_ee_pose_components(x=0.3, y=-0.1, z=0.4)  
    arm_2.arm.set_single_joint_position("waist", -math.pi/2.0)
    arm_2.gripper.open()                                    # Open gripper
    rospy.sleep(0.5)
    arm_2.arm.set_ee_cartesian_trajectory(x=-0.02, y=0, z=-0.18)     # Move to handover position

    # Wait for Arm 1 to release object (implement a proper sync if needed)
    #rospy.sleep(0.5)  # Simulating a delay for synchronization

    # Arm 2 closes its gripper to grasp the object
    arm_2.gripper.close()                                   # Close gripper to grab object
    rospy.sleep(3.5)
    #arm_2.arm.set_ee_cartesian_trajectory(x=0, y=0, z=0.2)            # Lift object

    # Arm 2 moves the object to a new location
    arm_2.arm.set_ee_pose_components(x=0.3, z=0.3)          # Move to a different position
    arm_2.arm.set_single_joint_position("waist", math.pi/2.0)
    rospy.sleep(0.5)

    arm_2.arm.set_ee_cartesian_trajectory(x=0, y=0, z=-0.195)
    rospy.sleep(0.5)

    arm_2.gripper.open()
    rospy.sleep(0.5)
    arm_2.arm.set_ee_cartesian_trajectory(x=0, y=0, z=0.3)
    rospy.sleep(0.5)
    arm_2.arm.set_single_joint_position("waist", 0)

    arm_2.arm.go_to_sleep_pose()
    arm_2.gripper.close()

def main():
    rospy.init_node("handover_example")

    # Start the two arms in parallel
    thread_1 = Thread(target=arm_1_pick_and_handover)
    thread_2 = Thread(target=arm_2_receive_and_move)
    thread_1.start()
    sleep(5.0)
    thread_2.start()

    thread_1.join()  # Wait for Arm 1 to finish
    thread_2.join()  # Wait for Arm 2 to finish

if __name__ == "__main__":
    main()
