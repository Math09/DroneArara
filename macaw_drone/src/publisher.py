#!/usr/bin/env python3

import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Empty

import sys, select, termios, tty

msg = """
+--------------------------------+
|        Teclas para mover       |
|                w               |
|        a       s       d       |
|        ------------------      |
|        l: alçar voo            |
|        g: descer drone         |
+--------------------------------+
"""

move = [

    'w',
    'd',
    's',
    'a',
    'l',
    'g'

]

def getKey():
    tty.setraw( sys.stdin.fileno() )
    select.select( [sys.stdin], [], [], 0 )
    key = sys.stdin.read( 1 )
    termios.tcsetattr( sys.stdin, termios.TCSADRAIN, settings )

    return key

if( __name__ == '__main__' ):
    settings = termios.tcgetattr( sys.stdin )
    rospy.init_node( 'publisher', anonymous=True )
    pub = rospy.Publisher( '/writing', String, queue_size=10 )

    print( msg )
    while( 1 ):
        key = getKey()
        if key in move:
            pub.publish( str( key ) )
        else:
            if key == '\x03':
                break
