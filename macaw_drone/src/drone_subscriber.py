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

speed = .5
turn = 1

moveBindings = {

    'w' : (1, 0, 0, 0),
    'd' : (1, 0, 0, -1),
    'a' : (1, 0, 0, 1),
    's' : (0, 0, 0, 1)

}

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

def move_forward_drone( moveBindings ):
    global message_move

    publish_cmd_vel = rospy.Publisher( '/drone/cmd_vel', Twist, queue_size=1 )

    x = moveBindings[0]
    y = moveBindings[1]
    z = moveBindings[2]
    th = moveBindings[3]

    message_move.linear.x = x * speed; message_move.linear.y = y * speed; message_move.linear.z = z * speed;
    message_move.angular.x = 0; message_move.angular.y = 0; message_move.angular.z = th * turn
    print('teste')
    publish_cmd_vel.publish( message_move )

def callback_drone( message ):
    global letter_move

    letter_move = message.data
    
def main():
    global letter_move
    global message_move

    rospy.init_node( 'drone_subscriber', anonymous=True )
    rospy.Subscriber( '/writing', String, callback_drone )

    publish_cmd_vel = rospy.Publisher( 'cmd_vel', Twist, queue_size=1 )

    rate = rospy.Rate( 50 )

    while not rospy.is_shutdown():
        if letter_move == 'g':
            land_drone()
        elif letter_move == 'l':
            takeoff_drone()
        else:
            if letter_move in moveBindings.keys():
                x = moveBindings[letter_move][0]
                y = moveBindings[letter_move][1]
                z = moveBindings[letter_move][2]
                th = moveBindings[letter_move][3]

                message_move.linear.x = x * speed; message_move.linear.y = y * speed; message_move.linear.z = z * speed;
                message_move.angular.x = 0; message_move.angular.y = 0; message_move.angular.z = th * turn

                publish_cmd_vel.publish( message_move )
                
        rate.sleep()

if( __name__ == '__main__' ):
    try:
        main()
    except rospy.ROSInterruptException:
        pass
