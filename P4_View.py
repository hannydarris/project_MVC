#====================================================================================
class View:
#====================================================================================
    def __init__(self):
        self.__size = 0
        self.__obj_dict = {}
        self.__maps = []
        self.__waypoints = {}

#====================================================================================
    def create(self, world_size):
        self.__size = world_size
        self.__maps = [[] for i in range(self.__size + 1)]
        for i in range(self.__size+1):
            for j in range(self.__size+1):
                waypoints_list = self.find_waypoint((i, j))
                if len(waypoints_list) == 1:
                    self.__maps[j].append('%s' % (waypoints_list[0].capitalize()))
                else:
                    self.__maps[j].append('.')

#====================================================================================
    def update_object(self, name, location):
        self.__obj_dict[name] = location

        # delete an object if location is None
        if location is None:
            del self.__obj_dict[name]

#====================================================================================
    def add_landmark(self, name, location):
        self.__waypoints[name] = location

#====================================================================================
    def draw(self):
        if self.__size != 0:
            self.create(self.__size)

        # create the grid map of the world
        for row in range(self.__size+1):
            for col in range(self.__size+1):
                object_list = self.find_object((row, col))

                if len(object_list) >= 2:
                    self.__maps[col][row] += '*  '
                elif len(object_list) == 1:
                    self.__maps[col][row] += object_list[0][0].capitalize() + '  '
                else:
                    self.__maps[col][row] += '   '

        # number the axes with multiples of 5
        for i in range(self.__size, -1,-1):
            if i % 5 == 0:
                print(format(i, '02d'), end='  ')
            else:
                print('    ', end='')
            for j in range(self.__size + 1):
                print(self.__maps[i][j], end="")
            print()
        print('    ',end='')

        for x in range(self.__size + 1):
            if x % 5 == 0:
                print(format(x, '02d'), end='  ')
            else:
                print('    ', end='')
        print()

#====================================================================================
    def find_object(self, location):
        objects = []
        for each in self.__obj_dict:
            # print(each)
            if location[0] == self.__obj_dict[each][0] and location[1] == self.__obj_dict[each][1]:
                objects.append(each)
        return objects

#====================================================================================
    def find_waypoint(self, location):
        waypoint = []
        for item in self.__waypoints:
            if location[0] == self.__waypoints[item][0] and location[1] == self.__waypoints[item][1]:
                waypoint.append(item)
        return waypoint

#====================================================================================
