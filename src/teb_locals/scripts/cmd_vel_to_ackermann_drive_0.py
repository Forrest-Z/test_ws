#!/usr/bin/env python

# Author: christoph.roesmann@tu-dortmund.de

import rospy, math, time
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped


def convert_trans_rot_vel_to_steering_angle(v, omega, wheelbase):
  if omega == 0 or v == 0:
    return 0
  
  radius = v / omega 
  rospy.loginfo("radius: %f", radius)
  return math.atan(wheelbase / radius)
  

def cmd_callback(data):
  global wheelbase
  global ackermann_cmd_topic
  global frame_id
  global pub
  global previous_steering_angle

  global large_change_angle_threshold
  global small_change_angle_threshold

  
  v = data.linear.x

  #steering_angle = convert_trans_rot_vel_to_steering_angle(v, data.angular.z, wheelbase)
  if abs(previous_steering_angle) ==  max_angle:
  	v = 0.2


  if data.angular.z != 0 and data.linear.x == 0:
    if data.angular.z > 0:
    	steering_angle =    max_angle
    else:
    	steering_angle =  - max_angle
    
  else:
    steering_angle = convert_trans_rot_vel_to_steering_angle(data.linear.x, data.angular.z, wheelbase)
    v = data.linear.x

  msg = AckermannDriveStamped()
  msg.header.stamp = rospy.Time.now()
  msg.header.frame_id = frame_id
  #msg.drive.steering_angle = steering * ((steering/max_angle)**2)
  msg.drive.steering_angle = steering_angle
  msg.drive.speed = v

  previous_steering_angle=steering_angle

  # cutportion=0.3
 

  # if(abs(steering_angle)<(cutportion*max_angle)):
  #   steering_angle=steering_angle*((steering_angle/(cutportion*max_angle))**2)
  #   msg.drive.steering_angle = steering_angle

  if msg.drive.steering_angle > max_angle:
    msg.drive.steering_angle = max_angle

  if msg.drive.steering_angle < -max_angle:
    msg.drive.steering_angle = -max_angle

  # if msg.drive.steering_angle != msg.drive.steering_angle:
  #   msg.drive.steering_angle = 0.0


  pub.publish(msg)

if __name__ == '__main__': 
  
  try:
    
    rospy.init_node('cmd_vel_to_ackermann_drive')
        
    twist_cmd_topic = rospy.get_param('~twist_cmd_topic', '/cmd_vel') 
    ackermann_cmd_topic = rospy.get_param('~ackermann_cmd_topic', '/ackermann_msg')
    wheelbase = rospy.get_param('~wheelbase', 1.48)
    frame_id = rospy.get_param('~frame_id', 'odom')
    max_angle = rospy.get_param("~max_angle", 1.5359)
    large_change_angle_threshold = rospy.get_param("~large_change_angle_threshold", 0.4)
    small_change_angle_threshold = rospy.get_param("~small_change_angle_threshold", 0.3)

    previous_steering_angle=0

    
    rospy.Subscriber(twist_cmd_topic, Twist, cmd_callback, queue_size=1)
    pub = rospy.Publisher(ackermann_cmd_topic, AckermannDriveStamped, queue_size=1)
    
    rospy.loginfo("Node 'cmd_vel_to_ackermann_drive' started.\nListening to %s, publishing to %s. Frame id: %s, wheelbase: %f", "/cmd_vel", ackermann_cmd_topic, frame_id, wheelbase)
    
    rospy.spin()
    
  except rospy.ROSInterruptException:
    pass

