# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy
import time
import random

from struct_game import *

map_rows, map_columns = 0, 0


def move_right(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if column+to_head+steps > (map_columns-1):
        return None
    #skontrolujem ci mam volnu cestu
    for i in range(1, steps+1):
        if stage.gmap[row][column+to_head+i] != 0:
            return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    #vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row][column +to_head-k] = 0
        new_map[row][column+to_head+steps-k] = vehicle.color
    # vyznacim novu poziciu, ked som to mal spolu s tymto cyklom hore tak sa to prepisovalo ak som robil iba napr 1krok
    new_stage.vehicles[vehicle.color - 1].column = column+steps
    return new_stage


def move_left(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if column - steps < 0:
        return None
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row][column - i] != 0:
            return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row][column + k] = 0
        new_map[row][column-steps+k]=vehicle.color
    new_stage.vehicles[vehicle.color - 1].column = column-steps
    return new_stage

def move_up(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if row - steps < 0:
        return None
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row - i][column] != 0:
            return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row + k][column] = 0
        new_map[row-steps+k][column]= vehicle.color
    new_stage.vehicles[vehicle.color - 1].row = row-steps
    return new_stage



def move_down(stage, vehicle, steps):
    row = vehicle.row
    column = vehicle.column
    to_head = vehicle.size - 1
    if row+to_head + steps > (map_rows-1):
        return None
    # skontrolujem ci mam volnu cestu
    for i in range(1, steps + 1):
        if stage.gmap[row + to_head + i][column] != 0:
            return None
    new_stage = copy.deepcopy(stage)
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(vehicle.size):
        new_map[row+to_head-k][column] = 0
        new_map[row+to_head+steps-k][column] = vehicle.color
    new_stage.vehicles[vehicle.color - 1].row = row+steps
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
    l = lines[1].split(" ")
    global map_rows
    global map_columns
    map_rows = int(l[0])
    map_columns = int(l[1])
    for line in lines[2:]:
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
        idstage = idstage*31 + (vehicle.color * vehicle.size + vehicle.column * vehicle.row)
        #idstage = idstage*31+counter * (vehicle.color * vehicle.size * vehicle.column * vehicle.row)
        counter += 1
    return idstage

def filter_node(node):
    parent = node.parents
    stage = node.stage
    while parent is not None:
        fstage = parent.stage
        i = 0
        matches = 0
        while i < len(fstage.vehicles):
            v1 = fstage.vehicles[i]
            v2 = stage.vehicles[i]
            if v1.row == v2.row and v1.column == v2.column and v1.color == v2.color:
                matches += 1
            i += 1
        # nasiel som zhodu
        if matches == len(fstage.vehicles):
            del stage  # neviem ci to usetri pamat heh...
            return False  # nie je unikatny


# NEVIEM CI TU NEBUDU KOLIZIE
def filter_stage(stage, processed_states):
    idstage = calculate_id(stage)
    stage.id = idstage
    found = processed_states.get(idstage)
    if found is None:
        return True
    else:
        # mam koliziu mozno ale porovnam proste este tie vozidla
        duplicate = False
        for fstage in found:
            i = 0
            matches = 0
            while i < len(fstage.vehicles):
                v1 = fstage.vehicles[i]
                v2 = stage.vehicles[i]
                if v1.row == v2.row and v1.column == v2.column and v1.color == v2.color:
                    matches +=1
                i+=1
            #nasiel som zhodu
            if matches == len(fstage.vehicles):
                del stage # neviem ci to usetri pamat heh...
                return False # nie je unikatny
        return True


def create_children(node, processed_states, children_list, que_l, search_type):
    global map_rows
    global map_columns
    for vehicle in node.stage.vehicles:
        row = vehicle.row
        column = vehicle.column
        stage = node.stage
        to_head = vehicle.size -1
        history = node.operator
        if vehicle.direction == 1:
            # je to game_columns-(min_size-1)-colum mozem sa posunut max o n-1 policok a este ked odpocitam
            # minimalnu dlzku auta co je 2 cize jedno policko uz mam vzdy automaticky ako keby tak n-2
            # dolava sa mozem posunut max o column 0-5 a doprava map_columns (velkost+1) - column
            if column < (map_columns-to_head-column):
                max_steps = map_columns-to_head-column
            else:
                max_steps = column

            for i in range(1, max_steps+1):
                if column + to_head < (map_columns-1):
                    # ked je zablokovane z oboch stran proste sa nikam nepohnem
                    if (column - 1 >= 0 and node.stage.gmap[row][column - 1] == 1) or (
                            column + 1 < 6 and node.stage.gmap[row][column + to_head + 1] == 1):
                        break

                if history is None or (not (history[0] == 'L' and history[1] == vehicle.color)):
                    stage = move_right(node.stage, vehicle, i)
                    # ak je unikatny ten stav, este som ho nespracoval
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ['R', vehicle.color, i], node.depth + 1)
                        if search_type == 1:  # breadth first
                            que_l.append(n)
                        else:  # depth first
                            que_l.insert(0, n)
                        #children_list.append(n)
                        if check_final(n):
                            return -1
                        #children_list.append(n)
                if history is None or not (history[0] == 'R' and history[1] == vehicle.color):
                    stage = move_left(node.stage, vehicle, i)
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ['L', vehicle.color, i], node.depth + 1)
                        if search_type == 1:  # breadth first
                            que_l.append(n)
                        else:  # depth first
                            que_l.insert(0, n)
                        #children_list.append(n)
                        if check_final(n):
                            return -1

        # VERTIKALNE
        else:
            if row < (map_rows-to_head-row):
                max_steps = map_rows-to_head-row
            else:
                max_steps = row
            for i in range(1,  max_steps+1):
                if row+to_head < (map_rows-1):
                    if (row - 1 >= 0 and node.stage.gmap[row-1][column] == 1) or (
                            row+ 1 < 6 and node.stage.gmap[row+to_head+1][column] == 1):
                        break
                if history is None or not (history[0] == 'D' and history[1] == vehicle.color):
                    stage = move_up(node.stage, vehicle, i)
                    # ak je unikatny ten stav, este som ho nespracoval
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ['U', vehicle.color, i], node.depth + 1)
                        #children_list.append(n)
                        if search_type == 1:  # breadth first
                            que_l.append(n)
                        else:  # depth first
                            que_l.insert(0, n)
                        if check_final(n):
                            return -1
                if history is None or not (history[0] == 'U' and history[1] == vehicle.color):
                    stage = move_down(node.stage, vehicle, i)
                    if stage is not None and filter_stage(stage, processed_states):
                        n = Node(stage, node, ['D', vehicle.color, i], node.depth + 1)
                        if search_type == 1:  # breadth first
                            que_l.append(n)
                        else:  # depth first
                            que_l.insert(0, n)
                        #children_list.append(n)
                        if check_final(n):
                            return -1
                        #
        #i += 1

    return 0


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
        found.insert(0,stage)


def search(que_l, processed_nodes, search_type):
    # que je uz prazdne a nenasiel som zatial riesenie takze neexistuje
    if len(que_l) == 0:
        return None
    i = 0
    counter = 0
    if check_final(que_l[0]):
        return que_l[0]
    while i < len(que_l):
        node = que_l.pop(0)
        children = []
        #print("Hlbka ", node.depth)
        ch_length = create_children(node, processed_nodes, children, que_l, search_type)
        #print("vygeneroval som potomkov")
        if ch_length == -1:
            if search_type == 1:
                end_node = que_l[-1]
            else:
                end_node = que_l[0]
            #end_node = children[-1]
            print("Pocet spracovanych uzlov", counter)
            print("Dlzka frontu na konci", len(que_l))
            return end_node
        #que_l.remove(node)
        add_to_processed(node.stage, processed_nodes)
        counter += 1
    return None


def print_steps(result_node):
    steps = []
    steps.insert(0, result_node.operator)
    parent = result_node.parent
    while parent is not None:
        if parent.operator is not None:
            steps.insert(0, parent.operator)
        parent = parent.parent
    print("Pocet krokov",len(steps))
    print(steps)
    print_map(result_node.parent.stage.gmap)
    print_map(result_node.stage.gmap)


def main(name):
    stage = load_stage("stav1.txt")
    #print_stage(stage)
    #print_map(stage.gmap)
    root = Node(stage, None, None, 0)
    #print_map(stage.gmap)
    root.stage.id = calculate_id(root.stage)
    que = [root] # que
    processed_nodes = {}
    # do sirky ma 1 do hlbky 0
    print("Hladanie do hlbky")
    start = time.time()
    result = search(que, processed_nodes, 0)
    if result is not None:
        print_steps(result)
    else:
        print("Skoncili sme neuspesne")
    end = time.time()
    print("Cas programu {:0.2f} s".format(end-start))
    print("Cas programu {:0.2f} minut".format((end - start)/60))

    que = [root]
    processed_nodes = {}
    print("Hladanie do sirky")
    start = time.time()
    result = search(que, processed_nodes, 1)
    if result is not None:
        print_steps(result)
    else:
        print("Skoncili sme neuspesne")
    end = time.time()
    print("Cas programu {:0.2f} s".format(end - start))
    print("Cas programu {:0.2f} minut".format((end - start) / 60))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
