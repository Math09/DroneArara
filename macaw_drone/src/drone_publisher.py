#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

import time
import sys
import math
import angles

from std_msgs.msg import Empty, String
from geometry_msgs.msg import Twist

letter_move = None
message_move = Twist()

def takeoff_drone():
    publish_takeoff = rospy.Publisher( '/drone/takeoff', Empty, queue_size=10 )
    message_takeoff = Empty()

    i = 0
    while( not i == 3 ):
        publish_takeoff.publish( message_takeoff )
        rospy.loginfo( 'Taking off..' )
        time.sleep( 1 )
        i += 1

def land_drone():
    publish_land = rospy.Publisher( '/drone/land', Empty, queue_size=10 )
    message_land = Empty()

    i = 0
    while( not i == 3 ):
        publish_land.publish( message_land )
        rospy.loginfo( 'Landing..' )
        time.sleep( 1 )
        i += 1

def move_forward_drone():
    global message_move

    rospy.loginfo( 'Moving forward.. ' )
    message_move.linear.x = 1.0
    message_move.angular.z = 0.0

    return message_move


def callback_drone( message ):
    global letter_move

    letter_move = message.data
    
def main():
    global letter_move
    global message_move

    rospy.init_node( 'drone', anonymous=True )
    rospy.Subscriber( '/writing', String, callback_drone )
    publish_cmd_vel = rospy.Publisher( '/drone/cmd_vel', Twist, queue_size=10 )

    rate = rospy.Rate( 15 )

    while not rospy.is_shutdown():
        if letter_move == 'A':
            land_drone()
        elif letter_move == 'L':
            takeoff_drone()
        elif letter_move == 'B':
            cmd_vel = move_forward_drone()
            publish_cmd_vel.publish( cmd_vel )
        else:
            print( 'sem letra' )

        rate.sleep()

if( __name__ == '__main__' ):
    try:
        main()
    except rospy.ROSInterruptException:
        pass
