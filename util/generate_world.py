import random
from adventure.models import Room, Player

names = ['Andrew', 'Matt', 'Ty', 'John', 'Roger', 'Raine', 'Pratchett', 'Liberty', 'Washington', 'Central', 'Main', 'Goliath', 'Demona', 'Angela', 'Brookylyn', 'Lexington', 'Broadway', 'Hudson', 'April', 'Shreder', 'Raphael', 'Leonardo', 'Michaelangelo', 'Donatello', 'Splinter', 'Bebop', 'Rocksteady', 'Fry', 'Bender', 'Zoidberg', 'Rocko', 'Dexter', 'Cartman', 'Wakko', 'Stimpy', 'Pinky', 'Taz', 'Chuckie', 'Hank Hill', 'Sonic', 'Batman', 'Joker', 'Godzilla', 'Spiderman', 'Wolverine', 'Megatron', 'Soundwave']

st_types = ['St.', 'Blvd.', 'Ave.', 'Pkwy', 'Square', "Lane", 'Way', 'Rd.']




def generate_rooms(size_x, size_y, num_rooms):
    Room.objects.all().delete()
    grid = [None] * size_y
    width = size_x
    height = size_y
    for i in range(len(grid)):
        grid[i] = [None] * size_x
    # Start from lower-left corner (0,0)
    x = -1  # (this will become 0 on the first step)
    y = 0
    room_count = 0
    direction = 1  # 1: east, -1: west
    while room_count < num_rooms:
        room_name = f"{random.choice(list(names))} {random.choice(list(st_types))}"
        if x < size_x - 1:
            x += 1
        else:
            x = 0
            y += 1
        room = Room(title=room_name, description="As you drive, ")
        grid[y][x] = room
        room.x = x
        room.y = y
        room.save()
        room_count += 1
    reverse_dir = {'n':'s','e':'w', 's': 'n', 'w': 'e'}
    for row in grid:
        for room in row:
            connections = 0
            while connections < 2:
                x = room.x
                y = room.y
                dir_list = ['n', 'e', 's', 'w']
                if x == 0:
                    dir_list.remove('w')
                elif x == 9:
                    dir_list.remove('e')
                if y == 0:
                    dir_list.remove('s')
                elif y == 9:
                    dir_list.remove('n')
                if room.n_to != 0:
                    connections += 1
                    dir_list.remove('n')
                if room.s_to != 0:
                    connections += 1
                    dir_list.remove('s')
                if room.e_to != 0:
                    connections += 1
                    dir_list.remove('e')
                if room.w_to != 0:
                    connections += 1
                    dir_list.remove('w')
                if len(dir_list) == 0:
                    room_direction = None
                else:
                    connections += 1
                    room_direction = random.choice(list(dir_list))
                if room_direction == 'n':
                    rev = reverse_dir[room_direction]
                    connect = grid[y + 1][x]
                    room.connectRooms(
                        connect, room_direction)
                    connect.connectRooms(room, rev)
                if room_direction == 's':
                    rev = reverse_dir[room_direction]
                    connect = grid[y - 1][x]
                    room.connectRooms(
                        connect, room_direction)
                    connect.connectRooms(room, rev)
                if room_direction == 'e':
                    rev = reverse_dir[room_direction]
                    connect = grid[y][x + 1]
                    room.connectRooms(
                        connect, room_direction)
                    connect.connectRooms(room, rev)
                if room_direction == 'w':
                    rev = reverse_dir[room_direction]
                    connect = grid[y][x - 1]
                    room.connectRooms(
                        connect, room_direction)
                    connect.connectRooms(room, rev)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            directions = []
            room = grid[y][x]
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
    starting_room = grid[4][4]
    players=Player.objects.all()
    for p in players:
        p.currentRoom=starting_room.id
        p.save()

generate_rooms(10, 10, 100)