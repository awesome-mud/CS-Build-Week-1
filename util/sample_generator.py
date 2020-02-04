# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

import random
from name_generator import names
from name_generator import st_types


class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        while room_count < num_rooms:
            room_name = random.choice(list(names)) +' '+ random.choice(list(st_types))
            if x < size_x - 1:
                x += 1
            else:
                x = 0
                y += 1
            room = Room(room_count, room_name, "This is a generic room.", x, y)
            self.grid[y][x] = room
            room_count += 1

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                dir_list = ['n', 'e', 's', 'w']
                if x == 0:
                    dir_list.remove('w')
                elif x == 9:
                    dir_list.remove('e')
                if y == 0:
                    dir_list.remove('s')
                elif y == 9:
                    dir_list.remove('n')

                if self.grid[y][x].n_to:
                    dir_list.remove('n')
                if self.grid[y][x].s_to:
                    dir_list.remove('s')
                if self.grid[y][x].e_to:
                    dir_list.remove('e')
                if self.grid[y][x].w_to:
                    dir_list.remove('w')

                if len(dir_list) == 0:
                    room_direction = None
                else:
                    room_direction = random.choice(list(dir_list))

                if room_direction == 'n':
                    self.grid[y][x].connect_rooms(self.grid[y+1][x], room_direction)
                if room_direction == 's':
                    self.grid[y][x].connect_rooms(self.grid[y-1][x], room_direction)
                if room_direction == 'e':
                    self.grid[y][x].connect_rooms(self.grid[y][x+1], room_direction)
                if room_direction == 'w':
                    self.grid[y][x].connect_rooms(self.grid[y][x-1], room_direction)



        # if x is 0 cannot go west/ x is 9 cannot go east
        # if y is 0 cannot go south / y is 9 cannot go north


        # REBUILD
        # # While there are rooms to be created...
        # previous_room = None
        # while room_count < num_rooms:
        #     choice = random.choice(list(directions.keys()))
        #     # Calculate the direction of the room to be created
        #     if direction > 0 and x < size_x - 1:
        #         room_direction = "e"
        #         x += 1
        #     elif direction < 0 and x > 0:
        #         room_direction = "w"
        #         x -= 1
        #     else:
        #         # If we hit a wall, turn north and reverse direction
        #         room_direction = "n"
        #         y += 1
        #         direction *= -1

        #     # Create a room in the given direction
        #     room = Room(room_count, "A Generic Room", "This is a generic room.", x, y)
        #     # Note that in Django, you'll need to save the room after you create it

        #     # Save the room in the World grid
        #     self.grid[y][x] = room

        #     # Connect the new room to the previous room
        #     if previous_room is not None:
        #         previous_room.connect_rooms(room, room_direction)

        #     # Update iteration variables
        #     previous_room = room
        #     room_count += 1


    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
