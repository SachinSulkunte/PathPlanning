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

rospy.init_node('follow_wall')

while not rospy.is_shutdown():
    for i in range(0,8):
        vel_msg.angular.z = 0.3
        pub.publish(vel_msg)
        time.sleep(0.5)
    rospy.loginfo("Done Rotating")
    vel_msg.angular.z = 0.0
    pub.publish(vel_msg)
    rospy.loginfo("Stoppped")
    time.sleep(100)

rospy.spin()