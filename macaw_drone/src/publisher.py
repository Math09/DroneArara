#!/usr/bin/env python3

import rospy
import time
from std_msgs.msg import String
from std_msgs.msg import Empty

def takeoff_message():
    return "subindo drone"

def main():
    # pub_takeoff = rospy.Publisher( '/drone/takeoff', Empty, queue_size=10 )
    # mov_msg = Empty()
    # publisher = rospy.Publisher( '/drone/land', Empty, queue_size=10 )
    # pub_land = Empty()
    pub = rospy.Publisher( '/writing', String, queue_size=10 )
    
    pub_a = 'A'
    pub_b = 'B'
    pub_c = 'C'
    pub_d = 'D'
    pub_l = 'L'

    rospy.init_node( 'publisher', anonymous=True )

    # i = 0
    while not rospy.is_shutdown():
    #     while not i == 3:
    #         pub_takeoff.publish( mov_msg )
    #         rospy.loginfo( 'Taking off...' )
    #         time.sleep( 1 )
    #         i += 1
        
        pub.publish( pub_l )
        rospy.loginfo( "Takeoff drone.." )
        time.sleep( 1 )

        pub.publish( pub_a )
        rospy.loginfo( "Landing drone.." )
        time.sleep( 1 )

        pub.publish( pub_b )
        rospy.loginfo( "Move Forward.." )
        time.sleep( 3 )
    
        # publisher.publish( pub_land )
        # rospy.loginfo( "Moving drone.." )
        # rospy.Rate( 15 )

if( __name__ == '__main__' ):
    main()
