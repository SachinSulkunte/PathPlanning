#! /usr/bin/env python

import rospy
import numpy as np
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
vel_msg = Twist()

roll = pitch = yaw = 0.0
target = 90
kp=0.5
def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def rotate(pub, direction):
    global target
    
    if(direction == "CCW"):
        target = -90
    target_rad = target*math.pi/180
    while(abs(target_rad-yaw)>0.05):
        command.angular.z = kp * (target_rad-yaw)
        pub.publish(command)
        print("taeget={} current:{}", target,yaw)
        r.sleep()
    rospy.loginfo("Done Rotating")

def stop(pub):
    vel_msg = Twist()
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    pub.publish(vel_msg)

def turnCW(pub):
    rospy.loginfo("Turning CW")
    stop(pub)
    rotate(pub, "CW")
    stop(pub)
    vel_msg = Twist()

def turnCCW(pub):
    rospy.loginfo("Turning CCW")
    stop(pub)
    rotate(pub, "CW")
    stop(pub)
    vel_msg = Twist()

def moveForward(pub):
    rospy.loginfo("Moving Forward")
    vel_msg = Twist()
    vel_msg.linear.x = 0.2
    pub.publish(vel_msg)

def check():
    global pub
    rospy.init_node('follow_wall')
    odom_sub = rospy.Subscriber ('/odom', Odometry, get_rotation)

    r = rospy.Rate(10)

    # state variables
    left_wall = 0
    front_wall = 0

    stop(pub) # set all velocities to 0

    while not rospy.is_shutdown():
        scan = rospy.wait_for_message("scan", LaserScan)
        front = scan.ranges[1]
        left = scan.ranges[90]
        # define states
        if left <= 0.75:
            left_wall = 1
        else:
            left_wall = 0
        if front <= 0.75:
            front_wall = 1
        else:
            front_wall = 0

        if (left_wall == 0):
            turnCCW(pub)
        elif (left_wall == 1 and front_wall == 1):
            turnCW(pub)
        else:
            rospy.loginfo(front_wall left_wall)
            moveForward(pub)
        
    rospy.spin()

if __name__ == "__main__":
    check()