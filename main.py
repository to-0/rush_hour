# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import enum
import time

import numpy as numpy

from struct_game import *

class Movement(enum.Enum):
    left = 0
    right = 1
    up = 2
    down = 3

def move_right(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    new_stage = None
    if column+to_head+steps > 5:
        return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    #skontrolujem ci mam volnu cestu
    for i in range(1, steps+1):
        if stage.gmap[row][column+to_head+i] != 0:
            return None
    #vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row][column + k] = 0
    # vyznacim novu poziciu, ked som to mal spolu s tymto cyklom hore tak sa to prepisovalo ak som robil iba napr 1krok
    for k in range(vehicle.size):
        new_map[row][column + steps + k] = vehicle.color
    vehicle2 = new_stage.vehicles[vehicle.color - 1]
    vehicle2.column = column + steps
    return new_stage


def move_left(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if column - steps < 0:
        return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row][column - i] != 0:
            return None
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    # new_stage = Stage(stage.vehicles, stage.gmap)
    # new_map = new_stage.gmap
    for k in range(vehicle.size):
        new_map[row][column + k] = 0

    for k in range(vehicle.size):
        new_map[row][column - steps + k] = vehicle.color
    vehicle2 = new_stage.vehicles[vehicle.color - 1]
    vehicle2.column = column - steps
    return new_stage

def move_up(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    new_stage = None
    if row - steps < 0:
        return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row - i][column] != 0:
            return None
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row + k][column] = 0

    for k in range(vehicle.size):
        new_map[row - steps + k][column] = vehicle.color
    vehicle2 = new_stage.vehicles[vehicle.color - 1]
    vehicle2.row = row - steps
    return new_stage



def move_down(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    new_stage = None
    if row+to_head + steps > 5:
        return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row + to_head + i][column] != 0:
            return None
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row+ k][column] = 0

    for k in range(vehicle.size):
        new_map[row + steps + k][column] = vehicle.color
    vehicle2 = new_stage.vehicles[vehicle.color - 1]
    vehicle2.row = row + steps
    return new_stage


def check_final(node):
    vehicle = node.stage.vehicles[0]
    #print(vehicle.column)
    if vehicle.column == 4:
        return True
    to_head = vehicle.column+vehicle.size-1
    if to_head == 5:
        return True
    return False

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
        row_offset, column_offset = 0, 0
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

def calculate_id(stage):
    idstage = 0
    counter = 1
    for vehicle in stage.vehicles:
        idstage += counter * (vehicle.color * vehicle.size * vehicle.column * vehicle.row)
        counter += 1
    return idstage


# NEVIEM CI TU NEBUDU KOLIZIE
def filter_stage(stage, processed_states):
    idstage = calculate_id(stage)
    stage.id = idstage
    found = processed_states.get(idstage)
    if found is None:
        return True
    else:
        duplicate = False
        # mam koliziu mozno ale porovnam proste tie arrays...
        for fstage in found:
            # if numpy.array_equal(stage.gmap, fstage.gmap):
            #     duplicate = True
            #     #print("mam duplikat")
            #     break
            i = 0
            matches = 0
            while i < len(fstage.vehicles):
                v1 = fstage.vehicles[i]
                v2 = stage.vehicles[i]
                if v1.row == v2.row and v1.column == v2.column and v1.color == v2.color:
                    matches +=1
                i+=1
            if matches == len(fstage.vehicles):
                del stage # neviem ci to usetri pamat heh...
                return False # nie je unikatny
        if not duplicate:
            return True
        return False


def create_children(node, processed_states):
    children_list = []
    counter = 0
    for vehicle in node.stage.vehicles:
        row_offset = 0
        column_offset = 0
        row = vehicle.row
        column = vehicle.column
        stage = node.stage
        to_head = vehicle.size -1
        for i in range(1, 6):
            history = node.operator
            if vehicle.direction == 1:
                # ked je zablokovane z oboch stran proste sa nikam nepohnem
                if column+to_head < 5:
                    if (column - 1 >= 0 and node.stage.gmap[row][column-1] == 1) or (
                            column+1 < 6 and node.stage.gmap[row][column+to_head + 1] == 1):
                        break
                if history is None or (not (history[0] == "L" and history[1] == vehicle.color)): #and history[2] == i)
                    stage = move_right(node.stage, vehicle, i)
                    # ak je unikatny ten stav, este som ho nespracoval
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ["R", vehicle.color, i])
                        #print_map(n.stage.gmap)
                        # if check_final(n):
                        #     print("Yay")
                        #     exit(1)
                        children_list.append(n)
                if history is None or not (history[0] == "R" and history[1] != vehicle.color): # and history[2] != i
                    stage = move_left(node.stage, vehicle, i)
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ["L", vehicle.color, i])
                        #print_map(n.stage.gmap)
                        if check_final(n):
                            print("Yay")
                            exit(1)
                        children_list.append(n)
            else:
                # ked je zablokovane z oboch stran proste sa nikam nepohnem
                if row+to_head < 5:
                    if (row - 1 >= 0 and node.stage.gmap[row-1][column] == 1) or (
                            row+ 1 < 6 and node.stage.gmap[row+to_head+1][column] == 1):
                        break
                if history is None or not (history[0] == "D" and history[1] == vehicle.color): # and history[2] == i
                    stage = move_up(node.stage, vehicle, i)
                    # ak je unikatny ten stav, este som ho nespracoval
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ["U", vehicle.color, i])
                        #print_map(n.stage.gmap)
                        if check_final(n):
                            print("Yay")
                            exit(1)
                        children_list.append(n)
                if history is None or not (history[0] == "U" and history[1] != vehicle.color): # and history[2] != i
                    stage = move_down(node.stage, vehicle, i)
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ["D", vehicle.color, i])
                        #print_map(n.stage.gmap)
                        if check_final(n):
                            print("Yay")
                            exit(1)
                        children_list.append(n)
    return children_list




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
    print("-"*30)

# z kontroly viem ze je to unikatne
def add_to_processed(stage, processed_states):
    idstage = stage.id
    found = processed_states.get(idstage)
    if found is None:
        processed_states[idstage] = [stage]
    else:
        found.append(stage)


def search(que_l, processed_nodes, search_type):
    # que je uz prazdne a nenasiel som zatial riesenie takze neexistuje

    if len(que_l) == 0:
        return False
    i = 0
    counter = 0
    while i < len(que_l):
        counter += 1
        #print("spracovavany node v poradi " + str(counter))
        #print("Dlzka que"+str(len(que_l)))
        node = que_l[i]
        #node = que[i]
        #stav = move_right(node.stage,node.stage.vehicles[1],3)
        if check_final(node):
            print("SKONCILI SME DAB DAB")
            return True
        children = create_children(node, processed_nodes)
        #print(len(children))
        que_l.remove(node)
        #que_l = que_l[1:]
        add_to_processed(node.stage, processed_nodes)
        for child in children:
            if search_type == 1:
                que_l.append(child)
            else:
                que_l.insert(0, child)

    return False



def main(name):
    stage = load_stage("stav1.txt")
    #print_stage(stage)
    #print_map(stage.gmap)
    root = Node(stage, None, None)
    root.stage.id = calculate_id(root.stage)
    que = [root] # que
    processed_nodes = {}
    # do sirky ma 1 do hlbky 0
    start = time.time()
    if search(que, processed_nodes, 1):
        print("Skoncili sme uspesne")
    else:
        print("Skoncili sme neuspesne")
    end = time.time()
    print("Cas programu {:0.2f} s".format(end-start))
    print("Cas programu {:0.2f} minut".format((end - start)/60))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
