# project_MVU_Controller
# author: @hannydarris

#!---
# Program creates a 2D world simulation with user-defined dimensions.
#	Run P4_Controller.py to start.
#	Internal commands:
#	- create world <n>		| creates 2D world of n dimensions
#	- create human <name> <x> <y>	| creates human in world at coordinates (x,y)
#					| name must be alphabetical
#	- create robot <name> <x> <y>	| creates robot in world at coordinates (x,y)
#					| name must be alphanumeric
#	- create fire <name> <x> <y>	| creates fire in world at coordinates (x,y)
#					| name must be alphabetical
#	- create waypoint <name> <x> <y>| creates waypoint in world at coordinates (x,y)
#					| name must be single letter
#	- move <human/robot> <destination>	| move human or robot (addressed by name) one unit toward destination
#						| as time progresses, destination can be waypoint, fire, or coordinates
#
#	- quit				| exits running program. Y to confirm.
#!---
