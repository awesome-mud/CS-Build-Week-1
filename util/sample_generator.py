import random
from adventure.models import Room

names = ['Andrew', 'Matt', 'Ty', 'John', 'Roger', 'Raine', 'Pratchett', 'Liberty', 'Washington', 'Central', 'Main', 'Goliath', 'Demona', 'Angela', 'Brookylyn', 'Lexington', 'Broadway', 'Hudson', 'April', 'Shreder', 'Raphael', 'Leonardo', 'Michaelangelo', 'Donatello', 'Splinter', 'Bebop', 'Rocksteady', 'Fry', 'Bender', 'Zoidberg', 'Rocko', 'Dexter', 'Cartman', 'Wakko', 'Stimpy', 'Pinky', 'Taz', 'Chuckie', 'Hank Hill', 'Sonic', 'Batman', 'Joker', 'Godzilla', 'Spiderman', 'Wolverine', 'Megatron', 'Soundwave']

st_types = ['St.', 'Blvd.', 'Ave.', 'Pkwy', 'Square', "Lane", 'Way', 'Rd.']

Room.objects.all().delete()


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        while room_count < num_rooms:
            room_name = f"{random.choice(list(names))} {random.choice(list(st_types))}"
            if x < size_x - 1:
                x += 1
            else:
                x = 0
                y += 1
            room = Room(title=room_name, description="As you drive, ")
            self.grid[y][x] = room
            room.x = x
            room.y = y
            room.save()
            room_count += 1

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                room = self.grid[y][x]
                while room.connections < 2:
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
                        room.add_connection()
                        room_direction = random.choice(list(dir_list))

                    if room_direction == 'n':
                        self.grid[y][x].connectRoom(
                            self.grid[y+1][x], room_direction)
                    if room_direction == 's':
                        self.grid[y][x].connectRoom(
                            self.grid[y-1][x], room_direction)
                    if room_direction == 'e':
                        self.grid[y][x].connectRoom(
                            self.grid[y][x+1], room_direction)
                    if room_direction == 'w':
                        self.grid[y][x].connectRoom(
                            self.grid[y][x-1], room_direction)

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                directions = []
                room = self.grid[y][x]
                if room.n_to:
                    directions.append('north')
                if room.s_to:
                    directions.append('south')
                if room.e_to:
                    directions.append('east')
                if room.w_to:
                    directions.append('west')
                room.description += f"the streets continue to the {str(', ').join(directions)}."


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
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        while room_count < num_rooms:
            room_name = f"{random.choice(list(names))} {random.choice(list(st_types))}"
            if x < size_x - 1:
                x += 1
            else:
                x = 0
                y += 1
            room = Room(room_count, room_name, "As you drive, ", x, y, 0)
            self.grid[y][x] = room
            room_count += 1

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                room = self.grid[y][x]
                while room.connections < 2:
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
                        room.add_connection()
                        room_direction = random.choice(list(dir_list))

                    if room_direction == 'n':
                        self.grid[y][x].connectRooms(
                            self.grid[y+1][x], room_direction)
                        self.grid[y+1][x].add_connection()
                    if room_direction == 's':
                        self.grid[y][x].connectRooms(
                            self.grid[y-1][x], room_direction)
                        self.grid[y-1][x].add_connection()
                    if room_direction == 'e':
                        self.grid[y][x].connectRooms(
                            self.grid[y][x+1], room_direction)
                        self.grid[y][x+1].add_connection()
                    if room_direction == 'w':
                        self.grid[y][x].connectRooms(
                            self.grid[y][x-1], room_direction)
                        self.grid[y][x-1].add_connection()

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                directions = []
                room = self.grid[y][x]
                if room.n_to:
                    directions.append('north')
                if room.s_to:
                    directions.append('south')
                if room.e_to:
                    directions.append('east')
                if room.w_to:
                    directions.append('west')
                room.description += f"the streets continue to the {str(', ').join(directions)}."
                room.save()


w = World()
num_rooms = 100
width = 10
height = 10
w.generate_rooms(width, height, num_rooms)
w.print_rooms()
