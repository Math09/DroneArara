#!/usr/bin/python3

import rospy
import time
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

import sys, select, termios, tty

speed = .5
turn = 1
msg = """
    Teclas para mover
            w
    a       s       d
    ------------------
    q: levantar voo
"""

moveBindings = {

    'w' : (1, 0, 0, 0),
    'd' : (1, 0, 0, -1),
    'a' : (1, 0, 0, 1),
    's' : (0, 0, 0, 1)

}

class MoveDrone( object ):
    def stop_drone( self ):
        self._move_msg.linear.x = 0.0
        self._move_msg.angular.z = 0.0

    def takeoff( self ):
        self._pub_cmd_vel = rospy.Publisher( '/cmd_vel', Twist, queue_size=1 )
        self._move_msg = Twist()
        self._pub_takeoff = rospy.Publisher( '/drone/takeoff', Empty, queue_size=1 )
        self._takeoff_msg = Empty()

        ros_rate = rospy.Rate( 1 )
        
        i = 0
        while not i == 3:
            self._pub_takeoff.publish( self._takeoff_msg )
            time.sleep( 1 )
            i += 1

def getKey():
    tty.setraw( sys.stdin.fileno() )
    select.select( [sys.stdin], [], [], 0 )
    key = sys.stdin.read( 1 )
    termios.tcsetattr( sys.stdin, termios.TCSADRAIN, settings )

    return key

if( __name__ == "__main__" ):
    settings = termios.tcgetattr( sys.stdin )
    pub = rospy.Publisher( 'cmd_vel', Twist, queue_size=1 )
    rospy.init_node( 'flights' )
    move_drone = MoveDrone()

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        print( msg )
        while( 1 ):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key == 'q':
                move_drone.takeoff()
                move_drone.stop_drone()
            else:
                x = 0
                y = 0
                z = 0
                th = 0
                if( key == '\x03' ):
                    break
            
            twist = Twist()
            twist.linear.x = x * speed; twist.linear.y = y * speed; twist.linear.z = z * speed;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th * turn
            pub.publish( twist )
    except rospy.ROSInterruptException:
        pass

