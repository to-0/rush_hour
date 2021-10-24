import time

from struct_game import *

map_rows, map_columns = 0, 0
time_create_children = 0
time_filter = 0
time_move = 0
time_deep_copy =0
time_no_idea = 0
time_casting = 0

def copy_stage(stage):
    #vehicles = [vehicle[:] for vehicle in stage.vehicles]
    vehicles = stage.vehicles[:]
    game_map = [row[:] for row in stage.gmap]
    return Stage(vehicles, game_map)

def move_right(stage, vehicle, steps, row, column, color, size, to_head):
    global time_move
    global time_deep_copy
    global time_casting
    start = time.time()
    end_casting = time.time()
    time_casting += end_casting-start
    st = time.time()
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc-st
    new_map = new_stage.gmap
    #vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row][column +to_head-k] = '0'
        new_map[row][column+to_head+steps-k] = vehicle[0] #vehicle[0] je farba
    new_stage.vehicles[color-1] = vehicle[0]+vehicle[1]+vehicle[2]+str(column+steps)+vehicle[4]
    end = time.time()
    time_move += end-start
    return new_stage


def move_left(stage, vehicle, steps, row, column, color, size):
    global time_move
    global time_deep_copy
    global time_casting
    start = time.time()
    end_casting = time.time()
    time_casting += end_casting - start
    st = time.time()
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row][column + k] = '0'
        new_map[row][column-steps+k]=vehicle[0]
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + vehicle[2] + str(column - steps) + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage

def move_up(stage, vehicle, steps, row, column, color, size):
    global time_deep_copy
    global time_move
    start = time.time()
    st = time.time()
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row + k][column] = '0'
        new_map[row-steps+k][column]= vehicle[0]
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + str(row-steps) + vehicle[3] + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage


def move_down(stage, vehicle, steps, row, column, color, size, to_head):
    global time_deep_copy
    global time_move
    start = time.time()
    new_stage = copy_stage(stage)
    st = time.time()
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    for k in range(size):
        new_map[row+to_head-k][column] = '0'
        new_map[row+to_head+steps-k][column] = vehicle[0]
    #new_stage.vehicles[color- 1][2]= str(row+steps)
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + str(row + steps) + vehicle[3] + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage

def check_final(node):
    vehicle = node.stage.vehicles[0]
    if vehicle[3] == "4":
        return True
    return False

def load_stage2(name):
    f = open(name, "r")
    lines = f.readlines()
    vehicles = []
    l = lines[1].split(" ")
    global map_rows
    global map_columns
    map_rows = int(l[0])
    map_columns = int(l[1])
    game_map = [['0' for i in range(map_rows)] for j in range(map_columns)]
    for line in lines[2:]:
        column_offset = 0
        row_offset = 0
        line = line.strip('\n')
        line = line.split(" ")
        if line[0][0]=="#":
            continue
        vehicles.append([line])
        direction = line[4]
        if direction == "1":
            column_offset = 1
        else:
            row_offset = 1
        size = int(line[1])
        row = int(line[2])
        column = int(line[3])
        for i in range(size):
            r: int = row+i*row_offset
            c: int = column+i*column_offset
            game_map[r][c] = line[0]
    f.close()
    return Stage(vehicles, game_map)

def print_stage(stage):
    for vehicle in stage.vehicles:
        print("Farba "+str(vehicle[0]))
        print("Velkost "+str(vehicle[1]))
        print("Riadok " + str(vehicle[2]))
        print("Stlpec " + str(vehicle[3]))
        print("Orientacia " + str(vehicle[4]))
        print("-"*30)


def calculate_id(stage):
    #idstage = 0
    idstage = ""
    for vehicle in stage.vehicles:
        #vehicle[0] - farba, vehicle[1] - velkost, vehicle[2] - riadok, vehicle[3] - stlpec, vehicle[4] otocenie
        # idstage = idstage * 89 + (vehicle[1]*vehicle[0] * vehicle[3] + vehicle[0] * vehicle[2]*vehicle[1]) * vehicle[1]
        idstage += vehicle
    return idstage


# vrati true ak nie je duplikat, false ak je
def filter_stage(stage, processed_states):
    global time_filter
    start = time.time()
    idstage = "".join(stage.vehicles)
    stage.id = idstage
    found = processed_states.get(idstage)
    vehicles_length = len(stage.vehicles)
    if found is None:
        end = time.time()
        time_filter += (end - start)
        return True
    else:
        end = time.time()
        time_filter += (end - start)
        return False

def check_hash(hashstage, processed_nodes):
    if processed_nodes.get(hashstage) is None:
        return True
    return False

def create_moved_hash(vehicles, color, steps, direction):
    ids = vehicles[:]
    new_vehicle = ""
    vehicle = ids[color-1]
    if direction == 'R':
        new_vehicle = str(color)+vehicle[1]+vehicle[2]+str(int(vehicle[3])+steps)+vehicle[4]
    elif direction == 'L':
        new_vehicle = str(color) + vehicle[1] + vehicle[2] + str(int(vehicle[3]) - steps) + vehicle[4]
    elif direction == 'U':
        new_vehicle = str(color) + vehicle[1] + str(int(vehicle[2]) - steps) + vehicle[3] + vehicle[4]
    elif direction == 'D':
        new_vehicle = str(color) + vehicle[1] + str(int(vehicle[2]) + steps)+ vehicle[3] + vehicle[4]
    ids[color-1] = new_vehicle
    return "".join(ids)

def create_children(node, processed_states, que_l, search_type):
    global time_create_children
    start = time.time()
    global map_rows
    global map_columns
    count = 0
    for vehicle in node.stage.vehicles:
        row = int(vehicle[2])
        column = int(vehicle[3])
        to_head = int(vehicle[1]) - 1
        color = int(vehicle[0])
        size = int(vehicle[1])
        history = node.operator
        if vehicle[4] == "1":
            max_right = 0
            max_left = 0
            for i in range(1, map_columns):
                if column+to_head+i < map_columns and max_right != -1 and node.stage.gmap[row][column+to_head+i] == '0':
                    if history is None or (not (history[0] == 'L' and history[1] == vehicle[0])):
                        #hash_cars = create_moved_hash(node.stage.vehicles, color, i, 'R')
                        #if check_hash(hash_cars, processed_states):
                        stage = move_right(node.stage, vehicle, i, row, column, color, size, to_head)
                        # ak je unikatny ten stav, este som ho nespracoval
                        if filter_stage(stage, processed_states):
                            s = "R" + vehicle[0] + str(i)
                            n = Node(stage, node, s, node.depth + 1)
                            count += 1
                            add_to_created(n.stage, processed_states)
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
                            if check_final(n):
                                end = time.time()
                                time_create_children += (end - start)
                                return -1
                else:
                    max_right = -1
                if column-i >= 0 and max_left != -1 and node.stage.gmap[row][column-i] == '0':
                    if history is None or not (history[0] == 'R' and history[1] == vehicle[0]):
                        #hash_cars = create_moved_hash(node.stage.vehicles, color, i, 'L')
                        #if check_hash(hash_cars,processed_states):
                        stage = move_left(node.stage, vehicle, i, row, column, color, size)
                        if filter_stage(stage, processed_states):
                            s = "L" + vehicle[0] + str(i)
                            n = Node(stage, node, s, node.depth + 1)
                            count += 1
                            add_to_created(n.stage, processed_states)
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
                else:
                    max_left = -1
                if max_right == -1 and max_left == -1:
                    break
        # VERTIKALNE
        else:
            max_up = 0
            max_down = 0
            for i in range(1, map_rows):
                if row + to_head+i < map_rows and max_down != -1 and node.stage.gmap[row + to_head + i][column] == '0':
                    if history is None or not (history[0] == 'U' and history[1] == vehicle[0]):
                        #hash_cars = create_moved_hash(node.stage.vehicles, color, i, 'D')
                        #if check_hash(hash_cars, processed_states):
                        stage = move_down(node.stage, vehicle, i, row, column, color, size, to_head)
                        if filter_stage(stage, processed_states):
                            s = "D" + vehicle[0] + str(i)
                            n = Node(stage, node, s, node.depth + 1)
                            count += 1
                            add_to_created(n.stage, processed_states)
                            if search_type == 1:  # breadth first
                                if n not in que_l:
                                    que_l.append(n)
                            else:  # depth first
                                if n not in que_l:
                                    que_l.insert(0, n)

                else:
                    max_down = -1
                if row-i >= 0 and max_up != -1 and node.stage.gmap[row-i][column]=='0':
                    if history is None or not (history[0] == 'D' and history[1] == vehicle[0]):
                        #hash_cars = create_moved_hash(node.stage.vehicles, color, i, 'U')
                        #if check_hash(hash_cars, processed_states):
                        stage = move_up(node.stage, vehicle, i, row, column, color, size)
                        # ak je unikatny ten stav, este som ho nespracoval
                        if filter_stage(stage, processed_states):
                            s = "U" + vehicle[0] + str(i)
                            n = Node(stage, node, s, node.depth + 1)
                            count += 1
                            add_to_created(n.stage, processed_states)
                            if search_type == 1:  # breadth first
                                if n not in que_l:
                                    que_l.append(n)
                            else:  # depth first
                                if n not in que_l:
                                    que_l.insert(0, n)
                else:
                    max_up = -1

                if max_up == -1 and max_down ==-1:
                    break
    end = time.time()
    time_create_children += (end - start)
    return count


def print_map(gmap):
    for i in range(map_rows):
        s = ""
        for j in range(map_columns):
            s+=str(gmap[i][j]) +" "
        print(s)
    print("-"*30)

# z kontroly viem ze je to unikatne
def add_to_created(stage, created_states):
    # idstage = stage.id
    # found = processed_states.get(idstage)
    # if found is None:
    #     processed_states[idstage] = [stage]
    # else:
    #     found.insert(0, stage)
    idstage = stage.id
    #found = processed_states.get(idstage)
    created_states[idstage]=True


def mark_as_processed(node):
    delattr(node.stage, "gmap")
    delattr(node.stage, "vehicles")
    delattr(node.stage, "id")
    delattr(node, "depth")


def search(que_l, search_type):
    counter = 0
    processed_nodes = {}
    steps = []
    global time_no_idea
    depth = 0
    if check_final(que_l[0]):
        return que_l[0]
    while que_l:
        node = que_l.pop(0)
        if search_type == 0:
            #vynaram sa vyssie
            if depth > node.depth:
                # vycistim processed nodes, tam su posledne referencie na uzly ktore su hlbsie (na tie co su vyssie
                # mam este referencie cez node.parent cize tie mi zostanu v pamati)
                # ako momentalna hlbka cize sa vymazu tie objekty uplne (setrim pamat)
                processed_nodes = {}
                depth = node.depth
        else:
            if depth < node.depth:
                print("Hlbka", node.depth)
                depth = node.depth
        #print("Hlbka ", node.depth)
        add_to_created(node.stage, processed_nodes)
        ch_length = create_children(node, processed_nodes, que_l, search_type)
        sta = time.time()
        #print("vygeneroval som potomkov ",ch_length)
        #print(len(que_l))
        if ch_length == -1:
            if search_type == 1:
                end_node = que_l[-1]
            else:
                end_node = que_l[0]
            print("Pocet spracovanych uzlov", counter)
            print("Dlzka frontu na konci", len(que_l))
            print("Celkovy cas create_children ", time_create_children)
            print("Z toho cas kedy som filtroval ", time_filter)
            print("Cize cisty cas create_children ze sa iba hybem a skusam ", time_create_children-time_filter)
            print("Cas kedy sa HYBEM IBA", time_move)
            print("cas copy", time_deep_copy)
            steps.append(end_node.operator)
            return end_node
        counter += 1
        mark_as_processed(node)

        e = time.time()
        time_no_idea += e-sta
        steps.append(node.operator)
    return None


def print_steps(result_node):
    steps = []
    steps.insert(0, result_node.operator)
    parent = result_node.parent
    while parent is not None:
        if parent.operator is not None:
            steps.insert(0, parent.operator)
        parent = parent.parent
    print("Pocet krokov", len(steps))
    print(steps)
    print_map(result_node.stage.gmap)


def main():
    search_type = input("Hladanie do sirky 1 hladanie do hlbky 0 \n")
    file_name = input("Nazov suboru \n")
    stage = load_stage2(file_name)
    search_type = int(search_type)
    root = Node(stage, None, None, 0)
    que = [root]
    start = time.time()
    result = search(que, search_type)
    if result is not None:
        print_steps(result)
    else:
        print("Skoncili sme neuspesne")
    end = time.time()
    print("Cas programu {:0.2f} s".format(end - start))
    print("Cas programu {:0.2f} minut".format((end - start) / 60))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()