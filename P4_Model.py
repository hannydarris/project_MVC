#===============================================================================
# P4_Model.py
# Created by Anthony Hornof - 4-8-2016
# Modified by Danny Harris - 4-13-2016
# Version 0.1
# Implementation for Spring 2016 CIS 211 Project 2
# Derived in part from Dave Kieras' design and implementation of EECS 381 Proj 4
#===============================================================================
global the_model
from P4_Utility import *

class Model:
    '''
    The Model object keeps track of everything in the simulated world.
    Only one Model should be created in each run of the simulation.
    '''

    #===========================================================================
    def __init__(self):

        self.__humans = []
        self.__waypoints = []
        self.__robots = []
        self.__fires = []
        self.__objects = []
        self.__world_size = None
        self.__view = None
        self._time = 0


    #===========================================================================
    def __str__(self):
        if self.__world_size:
            message = "The world is of size " + str(self.__world_size) + "."
            for i in self.__objects:
                message += '\n' + str(i)
            print(message)
    #===========================================================================
    def get_time(self):
        return self._time

    #===========================================================================
    def get_world_size(self):
        return self.__world_size

    #===========================================================================
    def attach_view(self, v):
        self.__view = v

    #===========================================================================
    def notify_location(self, name, location):
        self.__view.update_object(name, location)

    #===========================================================================
    def get_valid_location(self, arg1, arg2=None):
        '''
        Determine if a location is in the world.  If yes, returns a tuple of ints.
        This function is made polymorphic by using "switch on type".

        Parameters: arg1 and arg2 are ints, OR
                    arg1 and arg2 are strings, OR
                    arg1 is a tuple of two ints, and no arg2 is provided, OR
                    arg1 is a tuple of two strings, and no arg2 is provided
        Returns:    a tuple of ints if the location is in the world
                    None otherwise.

        Examples of use if the world is of size 30:
        self.get_valid_location(10, 20) -> (10, 20)
        self.get_valid_location('10', '20') -> (10, 20)
        self.get_valid_location((10, 20)) -> (10, 20)
        self.get_valid_location('a', '20') -> None
        self.get_valid_location(1.0, 20) -> None
        '''
        if type(arg1) == tuple and arg2 is None:
            x = arg1[0]
            y = arg1[1]
            if type(x) == int and type(y) == int or x.isdigit() and y.isdigit():
                if int(x) <= self.__world_size and int(y) <= self.__world_size:
                    return tuple([int(x), int(y)])
                else:
                    return None
            else:
                return None

        elif type(arg1) == int and type(arg2) == int:
            if arg1 <= self.__world_size and arg2 <= self.__world_size:
                return tuple([arg1, arg2])
            else:
                return None

        elif type(arg1) == str and arg2 is None:
            location = tuple(arg1.split(","))
            if location[0].isdigit() and location[1].isdigit():
                if int(location[0]) <= self.__world_size and int(location[-1]) <= self.__world_size:
                    return tuple([int(location[0]), int(location[1])])
                else:
                    return None
            else:
                return None

        else:
            x = arg1
            y = arg2
            if str(x).isdigit() and str(y).isdigit():
                if int(x) <= self.__world_size and int(y) <= self.__world_size:
                    return tuple([int(x), int(y)])
                else:
                    return None
            else:
                return None

    #===========================================================================
    def create_sim_object(self, arg_list):
        '''
        Create a simulation object based on the contents of the arg_list.
        Parameters: arg_list, list of strings entered after "create" command
        Returns:    True for if the line cannot be parsed, False if it can be.

        The only assumption that can be made about the arg_list when entering
        this function is that there was at least one string in the command line
        after "create".
        '''

        MIN_WORLD_SIZE = 5
        MAX_WORLD_SIZE = 30

        # Continue here checking for all of the different objects that "create"
        # could be called to build.  For each, after checking for the string
        # that appeared after "create", make sure that any additional arguments
        # on the line are all permissable given the project specification.

        if arg_list[0] == "world":
            if len(arg_list) == 2:
                if self.__world_size is None:
                    if arg_list[1].isdigit():
                        if int(arg_list[1]) >= MIN_WORLD_SIZE and int(arg_list[1]) <= MAX_WORLD_SIZE:
                            self.__world_size = int(arg_list[1])
                            print("Creating world of size %s." % (self.__world_size))
                            self.__view.create(self.__world_size)
                        else:
                            raise BadMsgError("Error: World size is out of range.")
                    else:
                        raise BadLineError
                else:
                    raise BadMsgError("Error: World already exists.")
            else:
                raise BadLineError

        elif arg_list[0] == "human":
            if self.__world_size is None:
                raise BadMsgError("Error: A world must be created before any other objects.")
            else:
                if len(arg_list) == 4:
                    if self.get_object(arg_list[1].lower()) is None:
                        if arg_list[1].isalnum():
                            if self.get_valid_location(arg_list[2], arg_list[3]) is None:
                                raise BadMsgError("Error: Invalid location.")
                            else:
                                h1 = Human(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                # h1.__init__(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                self.__humans.append(h1)
                                self.__objects.append(h1)
                                self.notify_location(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                print("Creating human %s at location %s." % (h1.get_name().capitalize(), self.get_valid_location(arg_list[2], arg_list[3])))

                        else:
                            raise BadMsgError("Error: Name must be alphanumeric.")
                    else:
                        raise BadMsgError("Error: Object already exists with that name.")
                else:
                    raise BadMsgError("Error: Invalid command.")

        elif arg_list[0] == "robot":
            if self.__world_size is None:
                raise BadMsgError("Error: A world must be created before any other objects.")

            else:
                if len(arg_list) == 4:
                    if self.get_object(arg_list[1].lower()) is None:
                        if arg_list[1].isalnum():
                            if self.get_valid_location(arg_list[2], arg_list[3]) is None:
                                print("Error: Invalid location.")
                                return True
                            else:
                                r1 = Robot(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                self.__objects.append(r1)
                                self.__robots.append(r1)
                                self.notify_location(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                print("Creating robot %s at location %s." % (r1.get_name().capitalize(), r1.get_location()))
                                return False
                        else:
                            raise BadMsgError("Error: Name must be alphanumeric.")
                    else:
                        raise BadMsgError("Error: Object already exists with that name.")
                else:
                    raise BadMsgError("Error: Invalid command.")

        elif arg_list[0] == "waypoint":
            if self.__world_size is None:
                print("Error: A world must be created before any other objects.")
                return True
            else:
                if len(arg_list) == 4:
                    if self.get_object(arg_list[1].lower()) is None:
                        if len(arg_list[1]) == 1 and arg_list[1].isalpha():
                            if self.get_valid_location(arg_list[2], arg_list[3]) is None:
                                raise BadMsgError("Error: Invalid location.")
                            else:
                                w1 = Waypoint(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                self.__objects.append(w1)
                                self.__waypoints.append(w1)
                                self.__view.add_landmark(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                print("Creating waypoint %s at location %s." % (w1.get_name().capitalize(), w1.get_location()))
                                return False
                        else:
                            raise BadMsgError("Error: Name must be one letter.")
                    else:
                        raise BadMsgError("Error: Object already exists with that name.")
                else:
                    raise BadMsgError("Error: Invalid command.")

        elif arg_list[0] == "fire":
            if self.__world_size is None:
                raise BadMsgError("Error: A world must be created before any other objects.")
            else:
                if len(arg_list) == 4:
                    if self.get_object(arg_list[1].lower()) is None:
                        if arg_list[1].isalnum():
                            if self.get_valid_location(arg_list[2], arg_list[3]) is None:
                                raise BadMsgError("Error: Invalid location.")
                            else:
                                f1 = Fire(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                self.__objects.append(f1)
                                self.__fires.append(f1)
                                self.notify_location(arg_list[1], self.get_valid_location(arg_list[2], arg_list[3]))
                                print("Creating fire %s at location %s." % (f1.get_name().capitalize(), f1.get_location()))

                        else:
                            raise BadMsgError("Error: Name must be alphanumeric.")
                    else:
                        raise BadMsgError("Error: Object already exists with that name.")
                else:
                    raise BadMsgError("Error: Invalid command.")
        else:
            raise BadMsgError("Error: Invalid command.")


    #===========================================================================
    def get_human(self, name):
        '''
        # Takes a name string.  Looks for a human with that name.  If one exists,
        #   returns that human.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to a human object, or None
        '''

        for hum in self.__humans:
            if hum.get_name() == name:
                return hum
        else:
            return None

    #===========================================================================
    def get_robot(self, name):
        '''
        Takes a name string. Looks for a robot with that name.
        Returns that robot, if it exists.
        Returns None, if not.

        '''
        for robot in self.__robots:
            if robot.get_name() == name:
                return robot
        else:
            return None

    #===========================================================================
    def get_object(self, name):
        '''
        Takes a name string. Looks for any object in the simulation with that name.
        '''
        for item in self.__objects:
            if item.get_name() == name:
                return item
        else:
            return None

    #===========================================================================
    def get_fire(self, name):
        for i in self.__fires:
            if i.get_name() == name:
                return i
        else:
            return None

    #===========================================================================
    def get_waypoint_location(self, name):
        '''
        Takes a name string. Looks for a waypoint in the simulation with that name.
        Returns that location as a tuple, if found.
        Returns None otherwise.
        '''
        for item in self.__waypoints:
            if item.get_name() == name:
                return item.get_location()
        else:
            return None

    #===========================================================================
    def describe_all(self):
        '''
        Each of the simulation objects describes itself in text.
        ( ) -> None
        '''
        print("The contents of the world are as follows:")
        self.__str__()

    #===========================================================================
    def fire_at_location(self, location):
        for fire in self.__fires:
            if fire._location == location:
                return fire
        else:
            return None

    #===========================================================================
    def delete_fire(self, name):
        if self.get_fire(name)._strength == 0:
            self.get_fire(name)._location = None
            self.__fires.remove(self.get_fire(name))

    #===========================================================================
    def update(self):
        for i in self.__objects:
            i.update()

#===============================================================================
class Sim_Object:
    '''
    An object created in the simulation.
    (Humans, Robots, Waypoints, Fires, etc.)
    '''
    def __init__(self, name, location):
        self._name = name
        self._location = location

    def __str__(self):
        return self._name.capitalize() + " at location " + str(self._location)

    def get_name(self):
        return self._name

    def get_class_name(self):
        return type(self).__name__

    def get_location(self):
        return self._location

    def update(self):
        pass

#=================================================================================
class Traveler(Sim_Object):
    '''
     An object in the simulation which inherits from the Sim_Object class.
     '''

    def __init__(self, name, location):
        self._destination_list = []
        self._moving = False
        super().__init__(name, location)

    def journey_to(self, destination_list):
        if self._location[0] == the_model.get_valid_location(destination_list)[0] or self._location[1] == the_model.get_valid_location(destination_list)[1]:
            for dest in range(len(destination_list)-1):
                if the_model.get_waypoint_location(destination_list[dest]):
                    destination = the_model.get_valid_location(the_model.get_waypoint_location(destination_list[dest]))
                else:
                    destination = the_model.get_valid_location(destination_list[dest])

                if self.get_valid_destination(destination_list[dest], destination_list[dest+1]):
                    self._moving = True
                    self._destination_list.append(destination)
                else:
                    raise BadMsgError("Error: '%s' is not a valid location for this 'move'" % (dest))
            if len(self._destination_list) > 0:
                self.move_to(self.get_next_moving_location())
        else:
            raise BadMsgError("Error: '%s' is not a valid location for this 'move'" % (destination_list[0]))

    def get_valid_destination(self, current, destination):
        if current[0] == destination[0] or current[1] == destination[1]:
            return True
        else:
            return False

    def get_next_moving_location(self):
        # check to see if the traveler should move horizontally
        if self._location[0] == self._destination_list[0][0] and self._location[1] != self._destination_list[0][1]:
            if self._location[1] < self._destination_list[0][1]:
                return tuple((self._location[0], self._location[1]+1))
            else:
                return tuple((self._location[0], self._location[1]-1))
        # check to see if the traveler should move vertically
        elif self._location[1] == self._destination_list[0][1] and self._location[0] != self._destination_list[0][0]:
            if self._location[0] < self._destination_list[0][0]:
                next_loc = tuple([self._location[0]+1, self._location[1]])
                if self._location[0] == next_loc[0] and self._location[1] == next_loc[1]:
                    self._destination_list.remove(self._destination_list[0])
                else:
                    return next_loc
            else:
                return tuple((self._location[0]-1, self._location[1]))

    def move_to(self, location):
        if the_model.get_valid_location(location):
            x = int(location[0])
            y = int(location[1])
            self._location = tuple([x, y])
            if len(self._destination_list) == 0:
                print("%s %s arrived at location %s." % (self.get_class_name(), self.get_name(), str(self.get_location())))
                the_model.notify_location(self.get_name(), self.get_location())
            else:
                the_model.notify_location(self.get_name(), self.get_location())
        else:
            raise BadMsgError("Error: Invalid location.")

#=================================================================================
class Human(Traveler):
    '''
    A human in the simulation.
    '''
    def __str__(self):
        if self._moving:
            message = "Human " + super().__str__() + " moving to "
            for loc in range(len(self._destination_list)):
                message += str(self._destination_list[loc])
            return message
        else:
            return "Human " + super().__str__()

    def get_name(self):
        return self._name

    def update(self):
        if self._moving:
            if the_model.fire_at_location(self.get_next_moving_location()):
                self._moving = False
                print("%s stopping short of fire %s." % (self._name.capitalize(), the_model.fire_at_location(self.get_next_moving_location()).get_name()))
            else:
                self.move_to(self.get_next_moving_location())

#=================================================================================
class Robot(Traveler):
    '''
    A robot in the simulation.
    '''
    def __init__(self, name, location):
        self._extinguishing_fire = None
        super().__init__(name, location)

    def __str__(self):
        return "Robot " + super().__str__()

    def fight_fire(self, fire_object):
        self._extinguishing_fire = fire_object
        if self._extinguishing_fire:
            fire_object.reduce_strength()
            self._moving = False
        elif len(self._destination_list) > 0:
            self._moving = True

    def update(self):
        if self._moving:
            self.move_to(self.get_next_moving_location())
        elif the_model.fire_at_location(self._location):
            self.fight_fire(the_model.fire_at_location(self._location))

#=================================================================================
class Fire(Sim_Object):
    '''
    A fire in the simulation.
    '''
    def __init__(self, name, location):
        self._strength = 5
        self._extinguished = False
        super().__init__(name, location)

    def __str__(self):
        return "Fire " + super().__str__()

    def __del__(self):
        print("Fire %s has disappeared from the simulation." % (self.get_name()))

    def get_strength(self):
        return self._strength

    def reduce_strength(self):
        self._strength -= 1
        if self._strength == 0:
            self._extinguished = True
            self.__del__()

#=================================================================================
class Waypoint(Sim_Object):
     '''
     A waypoint in the simulation.
     '''
     def __str__(self):
         return "Waypoint " + super().__str__()

