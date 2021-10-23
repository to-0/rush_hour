import time

from struct_game import *

map_rows, map_columns = 0, 0
time_create_children = 0
time_filter = 0
time_move = 0
time_deep_copy =0

def copy_stage(stage):
    #vehicles = [vehicle[:] for vehicle in stage.vehicles]
    vehicles = stage.vehicles[:]
    game_map = [row[:] for row in stage.gmap]
    return Stage(vehicles, game_map)

def move_right(stage, vehicle, steps):
    global time_move
    global time_deep_copy
    start = time.time()
    size = int(vehicle[1])
    row = int(vehicle[2])
    column = int(vehicle[3])
    to_head = int(vehicle[1]) - 1
    color = int(vehicle[0])
    # if column+to_head+steps > (map_columns-1):
    #     return None
    #skontrolujem ci mam volnu cestu
    st = time.time()
    #new_stage = copy.deepcopy(stage)
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc-st
    new_map = new_stage.gmap
    #vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row][column +to_head-k] = 0
        new_map[row][column+to_head+steps-k] = color #vehicle[0] je farba
    # vyznacim novu poziciu, ked som to mal spolu s tymto cyklom hore tak sa to prepisovalo ak som robil iba napr 1krok
    #new_stage.vehicles[color - 1][3] = str(column+steps)
    new_stage.vehicles[color-1] = vehicle[0]+vehicle[1]+vehicle[2]+str(column+steps)+vehicle[4]
    end = time.time()
    time_move += end-start
    return new_stage


def move_left(stage, vehicle, steps):
    global time_move
    global time_deep_copy
    start = time.time()
    row = int(vehicle[2])
    column = int(vehicle[3])
    to_head = int(vehicle[1]) - 1
    color = int(vehicle[0])
    size = int(vehicle[1])
    #print(size)
    st = time.time()
    #new_stage = copy.deepcopy(stage)
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(int(vehicle[1])):
        if column+k == 6:
            print("Pls")
        new_map[row][column + k] = 0
        new_map[row][column-steps+k]=color
    #new_stage.vehicles[color - 1][3] = str(column-steps)
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + vehicle[2] + str(column - steps) + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage

def move_up(stage, vehicle, steps):
    global time_deep_copy
    global time_move
    start = time.time()
    row = int(vehicle[2])
    column = int(vehicle[3])
    to_head = int(vehicle[1]) - 1
    color = int(vehicle[0])
    size = int(vehicle[1])
    st = time.time()
    #new_stage = copy.deepcopy(stage)
    new_stage = copy_stage(stage)
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row + k][column] = 0
        new_map[row-steps+k][column]= color
    #new_stage.vehicles[color - 1][2] = str(row-steps)
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + str(row-steps) + vehicle[3] + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage


def move_down(stage, vehicle, steps):
    global time_deep_copy
    global time_move
    start = time.time()
    row = int(vehicle[2])
    column = int(vehicle[3])
    to_head = int(vehicle[1]) - 1
    color = int(vehicle[0])
    size = int(vehicle[1])
    # skontrolujem ci mam volnu cestu
    #new_stage = copy.deepcopy(stage)
    new_stage = copy_stage(stage)
    st = time.time()
    endc = time.time()
    time_deep_copy += endc - st
    new_map = new_stage.gmap
    # vycistim tu poziciu kde bolo auto a zaroven pridam novu poziciu
    for k in range(size):
        new_map[row+to_head-k][column] = 0
        new_map[row+to_head+steps-k][column] = color
    #new_stage.vehicles[color- 1][2]= str(row+steps)
    new_stage.vehicles[color - 1] = vehicle[0] + vehicle[1] + str(row + steps) + vehicle[3] + vehicle[4]
    end = time.time()
    time_move += end - start
    return new_stage


def check_final(node):
    vehicle = node.stage.vehicles[0]
    #print(vehicle.column)
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
    game_map = [[0 for i in range(map_rows)] for j in range(map_columns)]
    for line in lines[2:]:
        column_offset = 0
        row_offset = 0
        line = line.strip('\n')
        if line[0][0]=="#":
            continue
        vehicles.append(line)
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
            game_map[r][c] = int(line[0])
    f.close()
    return Stage(vehicles, game_map)

def load_stage(name):
    f = open(name, "r")
    lines = f.readlines()
    vehicles = []
    l = lines[1].split(" ")
    global map_rows
    global map_columns
    map_rows = int(l[0])
    map_columns = int(l[1])
    game_map = [[0 for i in range(map_rows)] for j in range(map_columns)]
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
        vehicles.append([color, size, row, column, direction])
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
    idstage = calculate_id(stage)
    stage.id = idstage
    found = processed_states.get(idstage)
    vehicles_length = len(stage.vehicles)
    if found is None:
        end = time.time()
        time_filter += (end - start)
        return True
    else:
        # mam koliziu mozno ale porovnam proste este tie vozidla
        for fstage in found:
            i = 0
            matches = 0
            while i < vehicles_length:
                v1 = fstage.vehicles[i] # budu rovnkakej farby lebo ich beriem z rovnakeho indexu
                v2 = stage.vehicles[i]
                if v1[2] != v2[2] or v1[3] != v2[3]:
                    break
                if v1[2] == v2[2] and v1[3] == v2[3]:
                    matches +=1
                i+=1
            #nasiel som zhodu
            if matches == len(fstage.vehicles):
                end = time.time()
                time_filter += (end-start)
                return False # nie je unikatny
        end = time.time()
        time_filter += (end - start)
        return True


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
        history = node.operator
        try1 = 0
        try2 = 0
        if vehicle[4] == "1":
            max_right = 0
            max_left = 0
            for i in range(1, map_columns):
                if column+to_head+i >= map_columns:
                    break
                if node.stage.gmap[row][column + to_head + i] != 0:
                    break
                max_right += 1
            for i in range(1, map_columns):
                if column-i < 0:
                    break
                if node.stage.gmap[row][column-i] != 0:
                    break
                max_left += 1
            max_steps = max(max_right, max_left)
            # zistim si ci je blokovane z jednej alebo z oboch stran
            if max_steps == 0:
                continue

            for i in range(1, max_steps+1):
                if history is None or (not (history[0] == 'L' and history[1] == vehicle[0])):
                    if i <= max_right:
                        stage = move_right(node.stage, vehicle, i)
                        # ak je unikatny ten stav, este som ho nespracoval
                        if filter_stage(stage, processed_states):
                            n = Node(stage, node, ['R', vehicle[0], i], node.depth+1)
                            count += 1
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
                            if check_final(n):
                                end = time.time()
                                time_create_children += (end-start)
                                return -1
                if history is None or not (history[0] == 'R' and history[1] == vehicle[0]) and try2 != -1:
                    if i<=max_left:
                        stage = move_left(node.stage, vehicle, i)
                        if filter_stage(stage, processed_states):
                            n = Node(stage, node, ['L', vehicle[0], i],node.depth +1)
                            count += 1
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
        # VERTIKALNE
        else:
            max_up = 0
            max_down = 0
            for i in range(1, map_rows):
                if row+to_head+i > map_rows-1:
                    break
                if node.stage.gmap[row + to_head + i][column] != 0:
                    break
                max_down += 1

            for i in range(1, map_rows):
                if row-i < 0:
                    break
                if node.stage.gmap[row - i][column] != 0:
                    break
                max_up += 1
            max_steps = max(max_up, max_down)
            if max_steps == 0:
                continue

            for i in range(1,  max_steps+1):
                if history is None or not (history[0] == 'D' and history[1] == vehicle[0]) and try1 != -1:
                    if i<=max_up:
                        stage = move_up(node.stage, vehicle, i)
                        # ak je unikatny ten stav, este som ho nespracoval
                        if filter_stage(stage, processed_states):
                            n = Node(stage, node, ['U', vehicle[0], i],node.depth+1)
                            count += 1
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
                if history is None or not (history[0] == 'U' and history[1] == vehicle[0]) and try2 != -1:
                    if i<=max_down:
                        stage = move_down(node.stage, vehicle, i)
                        if filter_stage(stage, processed_states):
                            n = Node(stage, node, ['D', vehicle[0], i],node.depth+1)
                            count += 1
                            if search_type == 1:  # breadth first
                                que_l.append(n)
                            else:  # depth first
                                que_l.insert(0, n)
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
def add_to_processed(stage, processed_states):
    idstage = stage.id
    found = processed_states.get(idstage)
    if found is None:
        processed_states[idstage] = [stage]
    else:
        found.insert(0, stage)
    delattr(stage, "gmap")

def search(que_l, search_type):
    counter = 0
    processed_nodes = {}
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
                print("Hlbka",node.depth)
                depth = node.depth
        #print("Hlbka ", node.depth)
        ch_length = create_children(node, processed_nodes, que_l, search_type)
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
            return end_node
        counter += 1
        add_to_processed(node.stage, processed_nodes)
        delattr(node.stage, "id")
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
    print_map(result_node.parent.stage.gmap)
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