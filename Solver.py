#!/usr/bin/env python

# Author(s):	Rosalind Ellis (rnellis@brandeis.edu)
#		Melanie Kaplan-Cohen (melaniek@brandeis.edu)
#		Jonas Tjahjadi (jtjahjad15@brandeis.edu)
#
# Algorithm idea:
#	Follow the left most wall until completion
#

import rospy
#from stdr_msgs.msg import LaserSensorMsg
from sensor_msgs.msg import LaserScan #for real turtlebot
from Tkinter import *
from geometry_msgs.msg import Twist

class Solver():

	# variables to follow wall
	min_left = .05 # in meters
	max_left = .1
	# variables for checking front
	min_front = .07
	
	def __init__(self, sensor_topic):
		rospy.init_node('solver')
		self.sensor_topic_name = sensor_topic
		move_forward_twist = Twist() # initialize move forward, will follow left wall
		turn_twist = Twist() # initialize turning, will turn when wall right in front
		move_forward_twist.linear.x = 0.5
		turn_twist.angular.z = 0.5
		## init publisher
		cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
		# init subscriber and left forward right lists
		self.left = []
		self.front = []
		self.right = []

	# Publishes move forward or turn
	def move(direction):
		# set up distances
		left = direction[0]
		right = direction[1]
		in_front = direction[2]
		# check if we should move forward
		forward = __check_move__(in_front)
		# check if robot needs to adjust 
		if (forward and (left < min_left or left > max_left)):
			__adjust__(left)
		elif (forward): # move forward 
			cmd_vel_pub(self.move_forward)
		elif (not forward): # have to turn
			cmd_vel_pub(self.turn_twist)

	# adjust to follow left wall
	def __adjust__(distance):
		# establish diagonal movement (only necessary here -- why its not global or init)
		go_left = Twist()
		go_left.angular.z = -0.2
		go_left.linear.x = 0.2
		# actually move
		cmd_vel_pub(go_left)

	# check if there is a wall in front
	def __check_move__(front):
		# check front
		if (front < min_front):
			return false
		else:
			return true

	def read_sensors_callback(self, msg):
		#read / return information
		print("Range array has " + str(len(msg.ranges)) + " elements.")
		print("Angle Increment is " + str(msg.angle_increment))
		print(str(len(msg.ranges) * msg.angle_increment))
		# start movement by calling scanners to interpret information
		#read_scanners()
		

	# should take in callback info and interpret it into forward, turn, out
	def read_scanners():
		self.left = min(msg.ranges[255:285])
		self.right = min(msg.ranges[75:105])
		self.front = min(zip(msg.ranges[345:360], msg.ranges[0:15]))
		# move given info
		move([left, right, front])

	def start(self):
		root = Tk()
		rospy.Subscriber(self.sensor_topic_name, LaserScan, self.read_sensors_callback)
		root.mainloop()

def main():
	rospy.init_node('solver')
	maze_solver = Solver("/robot0/laser_0")
	maze_solver.start()
	#TODO - create shutdown method for when maze finishes


if __name__ == '__main__':
	main()
		
		