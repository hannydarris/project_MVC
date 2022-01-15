#===============================================================================
# P3_Controller.py
# Created by Anthony Hornof - 4-8-2016
# Modified by Danny Harris - 4-13-2016
# Version 0.2
# Implementation for Spring 2016 CIS 211 Project 2
# Derived in part from Dave Kieras' design and implementation of EECS 381 Proj 4
#===============================================================================

import sys  # for argv
import os   # for os.path.isfile() and os.access()

import P4_Model
import P4_View
from P4_Utility import *

#===============================================================================
def main ():
#===============================================================================
# Create a global Model object and assign it to a global variable called "the_model"
# Create a local instance of a Controller and have it start the run() function.

    global the_model
    the_model = P4_Model.Model()
    P4_Model.the_model = the_model
    Controller_1 = Controller()
    Controller_1.run()

#===============================================================================
class Controller:
#===============================================================================
    '''
    The controller object handles user keyboard input and provides textual to
    the console.  It follows the model view-controller software design pattern.
    '''

    #===========================================================================
    def __init__(self):

        self.__input_filename = "commands.txt"
        self.__input_file_object = None
        self.__view = P4_View.View()
        the_model.attach_view(self.__view)

    #===========================================================================
    def run(self):
    #===========================================================================
        '''
        () -> None.
        Process the command lines for the human-robot simulation.
        '''

        print("Starting Human-Robot Interaction Simulation.")

        # Attempt to open an input file for an initial set of commands
        self.open_initial_input_file()

        #=======================================================================
        # Command loop
        while True:

            # Get the next line of input whether it is from the user or a file.
            line = self.get_next_input_line()
            line_list = line.lower().split()

            try:
                if len(line_list) > 0:

                    if line_list[0] == "open":
                        self.__input_filename = line_list[1]
                        self.open_input_file()
                    elif line_list[0] == "create":
                        the_model.create_sim_object(line_list[1:])
                    elif line_list[0] == "status":
                        the_model.describe_all()
                    elif line_list[0] == "quit":
                        if len(line_list) == 1:
                            print("Are you sure you want to quit? (Y/N)", end=' ')
                            confirm = ''
                            if self.__input_file_object:
                                confirm = self.get_next_input_line()
                                print("FILE> %s" % (confirm))
                            else:
                                confirm = input("> ")
                            if confirm.lower() == "y":
                                break
                        else:
                            raise BadLineError
                    elif line_list[0] == "go" and len(line_list) == 1:
                        if len(line_list) == 1:
                            the_model._time += 1
                            the_model.update()
                        else:
                            raise BadLineError
                    elif len(line_list) > 1 and (the_model.get_human(line_list[0]) or the_model.get_robot(line_list[0])):
                        self.do_human_robot_command(line_list)
                    elif line_list[0] == "show":
                        self.do_show_command()
                    else:
                        raise BadLineError
            except BadMsgError as err:
                print(err)
            except BadLineError:
                print("Unrecognized command: %s" % (line))


    #===========================================================================
    # Manage the command line input file
    #===========================================================================

    def get_next_input_line(self):
        '''
        ( ) -> string
        • Displays the prompt.
        • Returns the next line to be processed, or '' if there is no line.
        • Gets the next line of text either from an input file or from the user,
          depending on the current setting of current_input_mode.
        • When reading from an input file, and either a blank line or an end of file
          is encountered, close the input file and set the file object var to None.
        '''

        if self.__input_file_object:
            line = self.__input_file_object.readline().strip()
            if line:
                print("Time {} FILE> {}".format(the_model.get_time(), line))
                return line
            else:
                self.__input_file_object.close()
                print("Closing file {}.".format(self.__input_filename))
                self.__input_file_object = None
                return input("Time {} > ".format(the_model._time))

        else:
            return input("Time {} > ".format(the_model._time))

    #===========================================================================
    def open_initial_input_file(self):
        '''
        Attempt to open a file for an initial set of commands.
        ( ) -> None
        If a filename was entered as a command line argument, overwrite the
          controller's member variable with that new filename.
        '''
        if len(sys.argv) > 1 and sys.argv[1]:
            self.__input_filename = sys.argv[1]
        self.open_input_file()

    #===========================================================================
    def open_input_file(self):
        '''
        ( ) -> None
        Attempts to open the filename in the input file member variable to
          execute a set of commands.
        '''
        try:
            self.__input_file_object = open(self.__input_filename)
        except FileNotFoundError:
            print("Error: File %s not found." % (self.__input_filename))
        except PermissionError:
            print("Error: Could not open and read input file: %s" % (self.__input_filename))
        else:
            print("Reading file: %s" % (self.__input_filename))

    #===========================================================================
    def do_show_command(self):
        self.__view.draw()

    #===========================================================================

    def do_human_robot_command(self, args):
        '''
        Parameters: args, a list of arguments that is already confirmed to be
                          nonempty with the first argument a human in the model.
        Returns:    None (All errors are reported within, so no need to return
                          an error flag.)

        Processes the remainder of the arguments to insure that they at least
        represent valid locations on the map.  If they are valid,
        call the appropriate function calls in the model to build them.
        '''

        if args[1] == "move":
            if len(args) >= 4:
                if the_model.get_human(args[0]):
                    human = the_model.get_human(args[0])
                    human.journey_to(args[2:])
                elif the_model.get_robot(args[0]):
                    robot = the_model.get_robot(args[0])
                    robot.journey_to(args[2:])
                else:
                    raise BadMsgError("Error: Invalid move command.")
            elif len(args) == 3:
                if len(args[2]) == 1:
                    location = [the_model.get_waypoint_location(args[-1])]
                else:
                    location = args[2]
                if location:
                    if the_model.get_human(args[0]):
                        human = the_model.get_human(args[0])
                        human.journey_to(location[0])
                    elif the_model.get_robot(args[0]):
                        robot = the_model.get_robot(args[0])
                        robot.journey_to(location[0])
                else:
                    raise BadMsgError("Error: Waypoint does not exist.")
            else:
                raise BadMsgError("Error: Invalid move command.")
        elif args[1] == "stop":
            object = the_model.get_object(args[0])
            object._moving = False
            print("{} {} stopped at location {}.".format(object.get_class_name(), object.get_name(), object.get_location()))
        elif args[1] == "attack":
            if the_model.get_robot(args[0]):
                robot = the_model.get_robot(args[0])
                fire = the_model.get_fire(args[2])
                if robot.get_location() == fire.get_location():
                    robot._moving = False
                    robot.fight_fire(fire)
                else:
                    raise BadMsgError("Error: No Fire at location {}.".format(robot.get_location()))
            else:
                raise BadMsgError("Error: Invalid attack command.")
        else:
            raise BadMsgError("Error: Invalid human/robot command.")



#===============================================================================
main ()
#===============================================================================

