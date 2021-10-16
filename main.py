# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import enum
import random
from struct import *

class Movement(enum.Enum):
    left = 0
    right = 1
    up = 2
    down = 3

def move_right(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if stage.map[row][column + to_head:steps] == 0:
        new_map = stage.map[:][:]  # skopirujem celu mapu
        new_map[row][column:column + to_head] = 0
        new_map[row][column + steps:column + steps + to_head] = 1
        new_stage = copy.deepcopy(stage)
        vehicle2 = new_stage[vehicle.color]
        vehicle2.column = column + steps
        return Stage(new_stage, new_map)
    return None


def move_left(stage,vehicle,steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if stage.map[row][column - steps:column-1] == 0: ##auto by sa posunulo o x krokov a tym padom kontrolujem  cely ten
        #priestor az po zadnu cast auta (nie vratane)
        new_map = stage.map[:][:]  # skopirujem celu mapu
        new_map[row][column:column + to_head] = 0
        #teraz zaplnim miesto kde je to auto po posunuti
        new_map[row][column - steps:column-steps+vehicle.size] = 1
        new_stage = copy.deepcopy(stage)
        vehicle2 = new_stage[vehicle.color]
        vehicle2.column = column - steps
        return Stage(new_stage, new_map)
    return None


def check_coordinates(gmap, row_offset,column_offset, start_row, start_column):
    if start_row+row_offset > 5:
        return False
    if start_column+column_offset > 5:
        return False

    if row_offset == 0: #vertikalne
        for k in range(start_column, column_offset+column_offset):
            if gmap[start_row][k] != 0:
                return False
    else: #horizontalne
        for i in range(start_row, start_row+row_offset):
            if gmap[i][start_column] != 0:
                return False
    return True


def generate_vehicle(gmap,index):
    x = random.randint(0,5)
    y = random.randint(0,5)
    orientation = random.randint(0,1)
    size = random.randint(2, 3)
    row_offset = 0
    column_offset = 0
    if orientation == 0:
        column_offset = size-1
    else:
        row_offset = size-1

    while check_coordinates(gmap, row_offset, column_offset, y, x) is not True:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        orientation = random.randint(0, 1)
        size = random.randint(2, 3)
        row_offset = 0
        column_offset = 0
        if orientation == 0:
            column_offset = size - 1
        else:
            row_offset = size - 1
    #neviem ci sa toto prejavi aj mimo tej funckie ale asi hej
    #map[y:y+row_offset][x:x+column_offset] = 1
    if orientation == 0: #vertikalne
        for k in range(x, x+column_offset):
            gmap[y][k]=1
    else:
        for i in range(y, y+row_offset):
            gmap[i][x] = 1
    return Vehicle(index, size, y, x, Direction(orientation))

# def create_start_stage(n):
#     n,m = 6,6
#     gmap = [[0 for i in range(n)] for j in range(m)]
#     for i in range(6):
#         for j in range(6):
#             gmap[i][j] = 0
#     stage = Stage([], gmap)
#     for i in range(n):
#         vehicle = []
#         if i == 0:
#             column = random.randint(1, 3) #nechcem ho dat hned na koniec a ma velkost 2 cize do 3 max
#             row = random.randint(0, 5)
#             vehicle = Vehicle(0, 2, row, column, Direction.horizontal)
#             stage.vehicles.append(vehicle)
#             #stage.map[y][x:x+1] = 1 nefunguje
#             stage.map[row][column] = 1
#             stage.map[row][column+1] = 1
#             #zablokujem ho vzdy
#             size = random.randint(2, 3)
#             row_second = 0
#             if row+size-1 > 5:
#                 row_second = row-size+1
#             elif row-1 < 0:
#                 row_second = 0
#             else:
#                 row_second = row-1
#             x_second = column
#             vehicle2 = Vehicle(1, size, row_second, column+vehicle.size, Direction.vertical)
#             stage.vehicles.append(vehicle2)
#             #stage.map[y_second:y+size-1][x] = 1
#             for k in range(row_second, row_second+size):
#                 stage.map[k][column+vehicle.size] = 1
#         else:
#             vehicle = generate_vehicle(stage.map, i)
#             stage.vehicles.append(vehicle)
#     return stage
#     # red_vehicle = Vehicle(Color.red, 2, 3, 1, Direction.h)
#     # stage = Stage(red_vehicle)
#     # stage.stage.append(Vehicle(Color.orange, 2, 1, 1, Direction.h))
#     # stage.stage.append(Vehicle(Color.yellow, 3, 2, 1, Direction.v))
#     # stage.stage.append(Vehicle(Color.purple, 2, 5, 1, Direction.v))
#     # stage.stage.append(Vehicle(Color.green, 3, 2, 4, Direction.v))
#     # stage.stage.append(Vehicle(Color.gray, 2, 5, 5, Direction.h))
def check_final(node):
    return 0
def load_stage(name):
    f = open(name, "r")
    lines = f.readlines()
    vehicles = []
    game_map = [[0 for i in range(6)] for j in range(6)]
    for line in lines:
        line = line.strip('\n')
        line = line.split(" ")
        if line[0][0]=="#":
            continue
        color = int(line[0])
        size = int(line[1])
        row = int(line[2])
        column = int(line[3])
        direction = int(line[4])
        row_offset, column_offset = 0,0
        if direction == 1:
            column_offset = 1
        else:
            row_offset = 1
        vehicle = Vehicle(color, size, row, column, direction)
        for i in range(size):
            r: int = row+i*row_offset
            c: int = column+i*column_offset
            game_map[r][c] = color
        vehicles.append(vehicle)
    return Stage(vehicles, game_map)


def print_stage(stage):
    for vehicle in stage.vehicles:
        print("Farba "+str(vehicle.color))
        print("Velkost "+str(vehicle.size))
        print("Riadok " + str(vehicle.row))
        print("Stlpec " + str(vehicle.column))
        print("Orientacia " + str(vehicle.direction))
        print("-"*30)


def filter_stage(stage, processed_states):
    pass


def create_children(node, processed_states):
    children_list = []
    counter = 0
    for vehicle in node.vehicles:
        row_offset = 0
        column_offset = 0
        row = vehicle.row
        column = vehicle.column
        if vehicle.direction == Direction.horizontal:
            to_head = vehicle.size-1
            for i in range(6): #dopredu
                stage = move_right(node.stage, vehicle, i)
                if stage is not None:
                    if filter_stage(stage, processed_states) != 1:
                        operator = ['R', vehicle.color, i]
                        children_list.append(Node(stage, node, operator))


def process_node(que, processed_states):
    node = que[0]
    if check_final(node):
        return 1
    create_children(node, processed_states)


def print_map(gmap):
    for i in range(6):
        s = ""
        for j in range(6):
            s+=str(gmap[i][j]) +" "
        print(s)

def main(name):
    print(Direction.horizontal)
    print(Color(1))
    # print_stage(stage)
    # root = Node(stage, None)
    # processed_states = []
    # que = []
    # que.append(root)
    # # process_node(que, processed_states)
    stage = load_stage("stav1.txt")
    print_stage(stage)
    print_map(stage.map)
    root = Node(stage, None, None)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
